"""Docker container lifecycle management for devcontainer-cli."""

import hashlib
import os
import shutil
import subprocess
import sys

from .config import ProjectConfig


def _docker_cmd() -> str:
    """Return docker command, preferring podman if available."""
    if shutil.which("podman"):
        return "podman"
    return "docker"


def container_name(config: ProjectConfig) -> str:
    """Generate deterministic container name from project path.

    Format: wbdev-{md5(abs_project_path)[:8]}-{basename}
    """
    abs_path = os.path.abspath(config.project_dir)
    path_hash = hashlib.md5(abs_path.encode()).hexdigest()[:8]
    basename = os.path.basename(abs_path)
    return f"wbdev-{path_hash}-{basename}"


def container_state(name: str) -> str:
    """Get container state: 'missing', 'running', or 'stopped'."""
    docker = _docker_cmd()
    try:
        result = subprocess.run(
            [docker, "inspect", "--format", "{{.State.Running}}", name],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return "missing"
        output = result.stdout.strip()
        return "running" if output == "true" else "stopped"
    except FileNotFoundError:
        print("Error: docker/podman not found in PATH", file=sys.stderr)
        sys.exit(1)


def create_container(config: ProjectConfig) -> str:
    """Create a new container from the devcontainer config. Returns container name."""
    docker = _docker_cmd()
    name = container_name(config)
    dc = config.devcontainer

    cmd = [docker, "create", "--name", name, "-w", config.container_workspace, "-it"]

    # runArgs from devcontainer.json
    cmd.extend(dc.run_args)

    # Implicit project mount
    cmd.extend(["-v", f"{config.project_dir}:{config.container_workspace}"])

    # Explicit mounts from devcontainer.json
    for mount in dc.mounts:
        source = mount.get("source", "")
        target = mount.get("target", "")
        mount_type = mount.get("type", "bind")
        if not source or not target:
            continue
        # Skip mounts with non-existent source directories
        if mount_type == "bind" and not os.path.exists(source):
            print(f"  Warning: skipping mount, source not found: {source}", file=sys.stderr)
            continue
        mount_str = f"type={mount_type},source={source},target={target}"
        if mount.get("readonly"):
            mount_str += ",readonly"
        cmd.extend(["--mount", mount_str])

    # Container environment variables
    for key, value in dc.container_env.items():
        cmd.extend(["-e", f"{key}={value}"])

    # Override entrypoint to keep container alive
    cmd.extend(["--entrypoint", "sleep"])
    cmd.append(dc.image)
    cmd.append("infinity")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error creating container:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    return name


def start_container(name: str) -> None:
    """Start a stopped container."""
    docker = _docker_cmd()
    result = subprocess.run([docker, "start", name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error starting container:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def stop_container(name: str) -> None:
    """Stop a running container."""
    docker = _docker_cmd()
    result = subprocess.run([docker, "stop", name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error stopping container:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def remove_container(name: str) -> None:
    """Remove a container."""
    docker = _docker_cmd()
    result = subprocess.run([docker, "rm", "-f", name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error removing container:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


SENTINEL_PATH = "/var/.wbdev-post-create-done"


def run_post_create(config: ProjectConfig, name: str) -> None:
    """Run postCreateCommand if it hasn't been run yet."""
    post_cmd = config.devcontainer.post_create_command
    if not post_cmd:
        return

    docker = _docker_cmd()

    # Check sentinel
    check = subprocess.run(
        [docker, "exec", name, "test", "-f", SENTINEL_PATH],
        capture_output=True,
    )
    if check.returncode == 0:
        return

    print(f"  Running postCreateCommand: {post_cmd}")
    result = subprocess.run(
        [docker, "exec", "-w", config.container_workspace, name, "bash", "-c", post_cmd],
    )
    if result.returncode != 0:
        print("Error: postCreateCommand failed", file=sys.stderr)
        sys.exit(1)

    # Create sentinel
    subprocess.run(
        [docker, "exec", name, "touch", SENTINEL_PATH],
        capture_output=True,
    )


def exec_in_container(
    name: str,
    command: str,
    workdir: str | None = None,
    env: dict[str, str] | None = None,
    interactive: bool = False,
) -> int:
    """Execute a command inside the container. Returns exit code."""
    docker = _docker_cmd()
    cmd = [docker, "exec"]

    if interactive and sys.stdin.isatty():
        cmd.extend(["-it"])

    if workdir:
        cmd.extend(["-w", workdir])

    if env:
        for key, value in env.items():
            cmd.extend(["-e", f"{key}={value}"])

    cmd.append(name)
    cmd.extend(["bash", "-c", command])

    result = subprocess.run(cmd)
    return result.returncode


def save_container(name: str, image_tag: str, output_path: str) -> None:
    """Snapshot a container and export the image to a tar.gz file.

    1. docker commit <name> <image_tag>
    2. docker save <image_tag> | gzip > <output_path>
    """
    docker = _docker_cmd()

    # Commit container to image
    result = subprocess.run(
        [docker, "commit", name, image_tag],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error committing container:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Save image to tar.gz
    save_proc = subprocess.Popen(
        [docker, "save", image_tag],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    with open(output_path, "wb") as f:
        gzip_proc = subprocess.Popen(
            ["gzip"],
            stdin=save_proc.stdout,
            stdout=f,
            stderr=subprocess.PIPE,
        )
        if save_proc.stdout:
            save_proc.stdout.close()
        _, gzip_err = gzip_proc.communicate()
        _, save_err = save_proc.communicate()

    if save_proc.returncode != 0:
        print(f"Error saving image:\n{save_err.decode()}", file=sys.stderr)
        sys.exit(1)
    if gzip_proc.returncode != 0:
        print(f"Error compressing image:\n{gzip_err.decode()}", file=sys.stderr)
        sys.exit(1)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  Saved {output_path} ({size_mb:.1f} MB)")


def load_container_image(input_path: str) -> str:
    """Import a container image from a tar.gz file. Returns the loaded image tag."""
    docker = _docker_cmd()
    result = subprocess.run(
        [docker, "load", "-i", input_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error loading image:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Parse output like "Loaded image: wbdev-snapshot-cpp:latest"
    for line in result.stdout.strip().splitlines():
        if "Loaded image" in line:
            tag = line.split(":", 1)[1].strip()
            # Handle "Loaded image: tag" and "Loaded image ID: sha256:..."
            return tag

    print(f"Warning: could not parse loaded image tag from: {result.stdout}", file=sys.stderr)
    return ""


def exec_in_container_background(
    name: str,
    command: str,
    workdir: str | None = None,
    env: dict[str, str] | None = None,
) -> tuple[int, str]:
    """Run a command in the container in background (detached). Returns (exit_code, stderr)."""
    docker = _docker_cmd()
    cmd = [docker, "exec", "-d"]

    if workdir:
        cmd.extend(["-w", workdir])

    if env:
        for key, value in env.items():
            cmd.extend(["-e", f"{key}={value}"])

    cmd.append(name)
    cmd.extend(["bash", "-c", command])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stderr

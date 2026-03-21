"""CLI entry point for devcontainer-cli."""

import argparse
import os
import sys

from .config import build_config, ProjectConfig
from .container import (
    container_name,
    container_state,
    create_container,
    exec_in_container,
    load_container_image,
    remove_container,
    run_post_create,
    save_container,
    start_container,
    stop_container,
)
from .runner import list_launches, list_tasks, run_launch, run_task

# File extensions that indicate a tar.gz image file
_IMAGE_FILE_EXTENSIONS = (".tar.gz", ".tgz", ".tar")


# ANSI colors
def _color(code: int, text: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def green(text: str) -> str:
    return _color(32, text)


def yellow(text: str) -> str:
    return _color(33, text)


def red(text: str) -> str:
    return _color(31, text)


def bold(text: str) -> str:
    return _color(1, text)


def cyan(text: str) -> str:
    return _color(36, text)


def _build_config_from_args(args: argparse.Namespace) -> ProjectConfig:
    """Build ProjectConfig from parsed CLI arguments."""
    project_dir = os.path.abspath(args.project_dir)
    codestyle_dir = os.path.abspath(args.codestyle_dir)

    cli_vars: dict[str, str] = {}
    if args.var:
        for v in args.var:
            if "=" not in v:
                print(f"Error: --var must be KEY=VALUE, got: {v}", file=sys.stderr)
                sys.exit(1)
            key, value = v.split("=", 1)
            cli_vars[key] = value

    return build_config(
        project_dir=project_dir,
        codestyle_dir=codestyle_dir,
        language=args.language,
        cli_vars=cli_vars,
    )


def cmd_up(args: argparse.Namespace) -> None:
    config = _build_config_from_args(args)
    if args.image:
        image = args.image
        # If it looks like a file path, load it first
        if any(image.endswith(ext) for ext in _IMAGE_FILE_EXTENSIONS) or os.path.isfile(image):
            if not os.path.exists(image):
                print(red(f"Image file not found: {image}"), file=sys.stderr)
                sys.exit(1)
            print(f"Loading image from {bold(image)}...")
            tag = load_container_image(image)
            if not tag:
                print(red("Failed to determine image tag from loaded file."), file=sys.stderr)
                sys.exit(1)
            print(green(f"  Loaded image: {tag}"))
            image = tag
        config.devcontainer.image = image
    name = container_name(config)
    state = container_state(name)

    if state == "running" and not args.rebuild:
        print(green(f"Container {name} is already running."))
        return

    if args.rebuild and state != "missing":
        print(yellow(f"Rebuilding: removing existing container {name}..."))
        if state == "running":
            stop_container(name)
        remove_container(name)
        state = "missing"

    if state == "missing":
        print(f"Creating container {bold(name)}...")
        create_container(config)
        print(green("  Container created."))
        state = "stopped"

    if state == "stopped":
        print(f"Starting container {bold(name)}...")
        start_container(name)
        print(green("  Container started."))

    run_post_create(config, name)
    print(green("Ready."))


def cmd_down(args: argparse.Namespace) -> None:
    config = _build_config_from_args(args)
    name = container_name(config)
    state = container_state(name)

    if state == "missing":
        print(yellow("No container to remove."))
        return

    if state == "running":
        print(f"Stopping container {bold(name)}...")
        stop_container(name)

    print(f"Removing container {bold(name)}...")
    remove_container(name)
    print(green("Done."))


def cmd_stop(args: argparse.Namespace) -> None:
    config = _build_config_from_args(args)
    name = container_name(config)
    state = container_state(name)

    if state != "running":
        print(yellow(f"Container {name} is not running (state: {state})."))
        return

    print(f"Stopping container {bold(name)}...")
    stop_container(name)
    print(green("Stopped."))


def cmd_start(args: argparse.Namespace) -> None:
    config = _build_config_from_args(args)
    name = container_name(config)
    state = container_state(name)

    if state == "running":
        print(green(f"Container {name} is already running."))
        return
    if state == "missing":
        print(red("No container exists. Run 'up' first."))
        sys.exit(1)

    print(f"Starting container {bold(name)}...")
    start_container(name)
    print(green("Started."))


def cmd_status(args: argparse.Namespace) -> None:
    config = _build_config_from_args(args)
    name = container_name(config)
    state = container_state(name)

    color_fn = {"running": green, "stopped": yellow, "missing": red}.get(state, str)
    print(f"Container: {bold(name)}")
    print(f"State:     {color_fn(state)}")
    print(f"Project:   {config.project_dir}")
    print(f"Language:  {config.language}")


def cmd_exec(args: argparse.Namespace) -> None:
    config = _build_config_from_args(args)
    name = container_name(config)
    state = container_state(name)

    if state != "running":
        print(red(f"Container is not running (state: {state}). Run 'up' first."), file=sys.stderr)
        sys.exit(1)

    cmd_parts = [a for a in args.exec_command if a != "--"]
    command = " ".join(cmd_parts) if cmd_parts else "bash"
    exit_code = exec_in_container(
        name, command, workdir=config.container_workspace, interactive=True
    )
    sys.exit(exit_code)


def cmd_tasks(args: argparse.Namespace) -> None:
    config = _build_config_from_args(args)

    if args.tasks_command == "list":
        list_tasks(config)
    elif args.tasks_command == "run":
        name = container_name(config)
        state = container_state(name)
        if state != "running":
            print(
                red(f"Container is not running (state: {state}). Run 'up' first."),
                file=sys.stderr,
            )
            sys.exit(1)
        exit_code = run_task(config, name, args.label)
        sys.exit(exit_code)
    else:
        print("Usage: devcontainer-cli tasks {list|run LABEL}", file=sys.stderr)
        sys.exit(1)


def cmd_save(args: argparse.Namespace) -> None:
    config = _build_config_from_args(args)
    name = container_name(config)
    state = container_state(name)

    if state == "missing":
        print(red("No container exists. Run 'up' first."), file=sys.stderr)
        sys.exit(1)

    image_tag = f"wbdev-snapshot-{config.language}:latest"
    output_path = args.file or f"{config.language}-devenv.tar.gz"

    print(f"Saving container {bold(name)} as {bold(image_tag)}...")
    save_container(name, image_tag, output_path)
    print(green("Done."))


def cmd_launch(args: argparse.Namespace) -> None:
    config = _build_config_from_args(args)

    if args.launch_command == "list":
        list_launches(config)
    elif args.launch_command == "run":
        name = container_name(config)
        state = container_state(name)
        if state != "running":
            print(
                red(f"Container is not running (state: {state}). Run 'up' first."),
                file=sys.stderr,
            )
            sys.exit(1)
        exit_code = run_launch(config, name, args.name)
        sys.exit(exit_code)
    else:
        print("Usage: devcontainer-cli launch {list|run NAME}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    # Determine default codestyle dir: script location's parent
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_codestyle = script_dir

    parser = argparse.ArgumentParser(
        prog="devcontainer-cli",
        description="VS Code DevContainers without VS Code",
    )
    parser.add_argument(
        "--project-dir",
        default=os.getcwd(),
        help="Project directory (default: current directory)",
    )
    parser.add_argument(
        "--codestyle-dir",
        default=default_codestyle,
        help=f"Path to codestyle repo (default: {default_codestyle})",
    )
    parser.add_argument(
        "--language",
        choices=["cpp", "go", "python"],
        default=None,
        help="Language config to use (default: auto-detect)",
    )
    parser.add_argument(
        "--var",
        action="append",
        metavar="KEY=VALUE",
        help="Set a placeholder variable (repeatable)",
    )

    subparsers = parser.add_subparsers(dest="command")

    # up
    up_parser = subparsers.add_parser("up", help="Create and start container")
    up_parser.add_argument("--rebuild", action="store_true", help="Rebuild container from scratch")
    up_parser.add_argument("--image", default=None, help="Use a saved image (tar.gz file or docker image tag)")

    # down
    subparsers.add_parser("down", help="Stop and remove container")

    # stop
    subparsers.add_parser("stop", help="Stop container")

    # start
    subparsers.add_parser("start", help="Start existing stopped container")

    # status
    subparsers.add_parser("status", help="Show container state")

    # save
    save_parser = subparsers.add_parser("save", help="Save container state to tar.gz")
    save_parser.add_argument("file", nargs="?", default=None, help="Output file (default: <language>-devenv.tar.gz)")

    # exec
    exec_parser = subparsers.add_parser("exec", help="Run command inside container")
    exec_parser.add_argument("exec_command", nargs=argparse.REMAINDER, help="Command to run")

    # tasks
    tasks_parser = subparsers.add_parser("tasks", help="Manage tasks from tasks.json")
    tasks_sub = tasks_parser.add_subparsers(dest="tasks_command")
    tasks_sub.add_parser("list", help="List all tasks")
    tasks_run = tasks_sub.add_parser("run", help="Run a task by label")
    tasks_run.add_argument("label", help="Task label to run")

    # launch
    launch_parser = subparsers.add_parser("launch", help="Manage launch configurations")
    launch_sub = launch_parser.add_subparsers(dest="launch_command")
    launch_sub.add_parser("list", help="List launch configurations")
    launch_run = launch_sub.add_parser("run", help="Run a launch configuration")
    launch_run.add_argument("name", help="Launch configuration name")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "up": cmd_up,
        "down": cmd_down,
        "stop": cmd_stop,
        "start": cmd_start,
        "status": cmd_status,
        "save": cmd_save,
        "exec": cmd_exec,
        "tasks": cmd_tasks,
        "launch": cmd_launch,
    }

    handler = handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

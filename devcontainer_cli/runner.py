"""Task and launch configuration execution for devcontainer-cli."""

import os
import shlex
import sys

from .config import (
    ProjectConfig,
    find_unresolved_placeholders,
    load_jsonc,
    prompt_for_variables,
    resolve_variables,
)
from .container import exec_in_container, exec_in_container_background


def _task_group_label(group: str | dict) -> str:
    """Extract group kind from task group field."""
    if isinstance(group, dict):
        return group.get("kind", "")
    return group


def load_tasks(config: ProjectConfig) -> list[dict]:
    """Load tasks from tasks.json, merging codestyle and project-local tasks."""
    tasks: list[dict] = []
    global_env: dict[str, str] = {}

    # Load from codestyle language-specific tasks.json
    codestyle_tasks_path = os.path.join(config.vscode_dir(), "tasks.json")
    if os.path.exists(codestyle_tasks_path):
        data = load_jsonc(codestyle_tasks_path)
        # Extract global options.env (Go has this)
        options = data.get("options", {})
        global_env = options.get("env", {})
        tasks.extend(data.get("tasks", []))

    # Load from project-local tasks.json (project overrides codestyle)
    project_tasks_path = os.path.join(config.project_dir, ".vscode", "tasks.json")
    if os.path.exists(project_tasks_path):
        data = load_jsonc(project_tasks_path)
        options = data.get("options", {})
        proj_env = options.get("env", {})
        global_env.update(proj_env)
        existing_labels = {t.get("label"): i for i, t in enumerate(tasks)}
        for task in data.get("tasks", []):
            label = task.get("label")
            if label in existing_labels:
                tasks[existing_labels[label]] = task
            else:
                tasks.append(task)

    # Merge global env into each task
    for task in tasks:
        task_options = task.get("options", {})
        task_env = task_options.get("env", {})
        merged_env = dict(global_env)
        merged_env.update(task_env)
        if merged_env:
            task.setdefault("options", {})["env"] = merged_env

    return tasks


def _find_task(tasks: list[dict], label: str) -> dict | None:
    """Find a task by label."""
    for t in tasks:
        if t.get("label") == label:
            return t
    return None


def resolve_task_order(tasks: list[dict], label: str) -> list[str]:
    """DFS topological sort on dependsOn graph. Returns execution order."""
    visited: set[str] = set()
    in_stack: set[str] = set()
    order: list[str] = []

    def dfs(current_label: str) -> None:
        if current_label in visited:
            return
        if current_label in in_stack:
            print(f"Error: dependency cycle detected at task '{current_label}'", file=sys.stderr)
            sys.exit(1)

        task = _find_task(tasks, current_label)
        if task is None:
            print(f"Error: task '{current_label}' not found", file=sys.stderr)
            sys.exit(1)

        in_stack.add(current_label)

        deps = task.get("dependsOn", [])
        depends_order = task.get("dependsOrder", "parallel")

        if depends_order == "sequence":
            # Run dependencies in order as listed
            for dep in deps:
                dfs(dep)
        else:
            # Parallel order — still need to resolve all deps
            for dep in deps:
                dfs(dep)

        in_stack.discard(current_label)
        visited.add(current_label)
        order.append(current_label)

    dfs(label)
    return order


def _build_task_command(task: dict, config: ProjectConfig) -> str:
    """Build the shell command for a task, resolving variables."""
    ctx = config.make_variable_context()
    command = task.get("command", "")
    args = task.get("args", [])

    command = resolve_variables(command, ctx)

    if args:
        resolved_args = [resolve_variables(str(a), ctx) for a in args]
        command = command + " " + " ".join(resolved_args)

    return command


def _build_task_env(task: dict, config: ProjectConfig) -> dict[str, str]:
    """Build environment variables for a task."""
    ctx = config.make_variable_context()
    env: dict[str, str] = {}
    task_options = task.get("options", {})
    task_env = task_options.get("env", {})
    for k, v in task_env.items():
        env[k] = resolve_variables(str(v), ctx)
    return env


def _build_task_cwd(task: dict, config: ProjectConfig) -> str | None:
    """Build working directory for a task."""
    ctx = config.make_variable_context()
    task_options = task.get("options", {})
    cwd = task_options.get("cwd")
    if cwd:
        return resolve_variables(cwd, ctx)
    return None


def run_task(config: ProjectConfig, container: str, label: str) -> int:
    """Run a task by label, resolving dependencies first. Returns exit code."""
    tasks = load_tasks(config)

    # Check task exists
    task = _find_task(tasks, label)
    if task is None:
        print(f"Error: task '{label}' not found", file=sys.stderr)
        available = [t.get("label", "") for t in tasks]
        print(f"Available tasks: {', '.join(available)}", file=sys.stderr)
        return 1

    # Resolve all variables needed for the full task chain
    order = resolve_task_order(tasks, label)

    # Check for unresolved placeholders and prompt if needed
    ctx = config.make_variable_context()
    all_commands = ""
    for task_label in order:
        t = _find_task(tasks, task_label)
        if t:
            all_commands += " " + t.get("command", "")
            all_commands += " " + " ".join(str(a) for a in t.get("args", []))

    needed = find_unresolved_placeholders(resolve_variables(all_commands, ctx))
    if needed:
        print("Some variables need to be set:")
        config.user_vars = prompt_for_variables(needed, config.user_vars)

    # Execute tasks in dependency order
    for task_label in order:
        t = _find_task(tasks, task_label)
        if t is None:
            continue

        command = _build_task_command(t, config)
        env = _build_task_env(t, config)
        cwd = _build_task_cwd(t, config)
        is_background = t.get("isBackground", False)

        print(f"\n  Running task: {task_label}")
        print(f"  Command: {command}")

        if is_background:
            workdir = cwd or config.container_workspace
            exit_code, stderr = exec_in_container_background(
                container, command, workdir=workdir, env=env
            )
            if exit_code != 0:
                print(f"  Error starting background task: {stderr}", file=sys.stderr)
                return exit_code
            print("  Started in background.")
        else:
            workdir = cwd or config.container_workspace
            exit_code = exec_in_container(
                container, command, workdir=workdir, env=env, interactive=True
            )
            if exit_code != 0:
                print(f"  Task '{task_label}' failed with exit code {exit_code}", file=sys.stderr)
                return exit_code

    return 0


def list_tasks(config: ProjectConfig) -> None:
    """Pretty-print all available tasks."""
    tasks = load_tasks(config)
    if not tasks:
        print("No tasks found.")
        return

    print(f"Tasks ({len(tasks)}):\n")
    for task in tasks:
        label = task.get("label", "<unnamed>")
        group = task.get("group", "")
        group_str = _task_group_label(group)
        deps = task.get("dependsOn", [])

        line = f"  {label}"
        if group_str:
            line += f"  [{group_str}]"
        if deps:
            line += f"  (depends: {', '.join(deps)})"
        if task.get("isBackground"):
            line += "  [background]"
        print(line)


def load_launch_configs(config: ProjectConfig) -> list[dict]:
    """Load launch configurations from launch.json."""
    configs: list[dict] = []

    # Load from codestyle language-specific launch.json
    codestyle_launch_path = os.path.join(config.vscode_dir(), "launch.json")
    if os.path.exists(codestyle_launch_path):
        data = load_jsonc(codestyle_launch_path)
        configs.extend(data.get("configurations", []))

    # Load from project-local launch.json (project overrides codestyle)
    project_launch_path = os.path.join(config.project_dir, ".vscode", "launch.json")
    if os.path.exists(project_launch_path):
        data = load_jsonc(project_launch_path)
        existing_names = {c.get("name"): i for i, c in enumerate(configs)}
        for lc in data.get("configurations", []):
            name = lc.get("name")
            if name in existing_names:
                configs[existing_names[name]] = lc
            else:
                configs.append(lc)

    return configs


def _find_launch_config(configs: list[dict], name: str) -> dict | None:
    """Find a launch config by name."""
    for c in configs:
        if c.get("name") == name:
            return c
    return None


def run_launch(config: ProjectConfig, container: str, name: str) -> int:
    """Run a launch/debug configuration. Returns exit code."""
    launch_configs = load_launch_configs(config)
    lc = _find_launch_config(launch_configs, name)
    if lc is None:
        print(f"Error: launch configuration '{name}' not found", file=sys.stderr)
        available = [c.get("name", "") for c in launch_configs]
        print(f"Available: {', '.join(available)}", file=sys.stderr)
        return 1

    ctx = config.make_variable_context()

    # Check for unresolved placeholders
    import json as json_mod

    lc_text = json_mod.dumps(lc)
    needed = find_unresolved_placeholders(resolve_variables(lc_text, ctx))
    if needed:
        print("Some variables need to be set:")
        config.user_vars = prompt_for_variables(needed, config.user_vars)
        ctx = config.make_variable_context()

    # Run preLaunchTask if specified
    pre_task = lc.get("preLaunchTask")
    if pre_task:
        pre_task = resolve_variables(pre_task, ctx)
        print(f"Running preLaunchTask: {pre_task}")
        exit_code = run_task(config, container, pre_task)
        if exit_code != 0:
            return exit_code

    lc_type = lc.get("type", "")
    mode = lc.get("mode", "")

    if lc_type == "cppdbg":
        return _run_cppdbg(config, container, lc, ctx)
    elif lc_type == "go" and mode == "remote":
        return _run_go_remote(config, container, lc, ctx)
    else:
        print(f"Unsupported launch type: {lc_type} (mode: {mode})", file=sys.stderr)
        return 1


def _run_cppdbg(
    config: ProjectConfig, container: str, lc: dict, ctx: dict[str, str]
) -> int:
    """Run a C++ debug configuration using gdb."""
    program = resolve_variables(lc.get("program", ""), ctx)
    setup_commands = lc.get("setupCommands", [])
    pipe_transport = lc.get("pipeTransport")
    mi_debugger_addr = lc.get("miDebuggerServerAddress")

    # Determine debugger path
    linux_config = lc.get("linux", {})
    debugger_path = linux_config.get("miDebuggerPath", "gdb-multiarch")

    # Build GDB command
    gdb_args = [debugger_path, "-q"]

    # Add setup commands as -ex arguments
    for cmd in setup_commands:
        text = cmd.get("text", "")
        if text:
            text = resolve_variables(text, ctx)
            gdb_args.extend(["-ex", text])

    if pipe_transport:
        # Remote debug via SSH pipe: connect local gdb to remote gdbserver
        pipe_program = pipe_transport.get("pipeProgram", "/usr/bin/ssh")
        pipe_args = pipe_transport.get("pipeArgs", [])

        resolved_pipe_args = [resolve_variables(str(a), ctx) for a in pipe_args]
        ssh_target = " ".join(resolved_pipe_args)
        target_cmd = f"target remote | {pipe_program} {ssh_target} gdbserver - {program}"
        gdb_args.extend(["-ex", target_cmd])
        gdb_args.append(program)

    elif mi_debugger_addr:
        # Local QEMU debug
        addr = resolve_variables(mi_debugger_addr, ctx)
        gdb_args.extend(["-ex", f"target remote {addr}"])
        gdb_args.append(program)

    else:
        gdb_args.append(program)

    command = " ".join(shlex.quote(a) for a in gdb_args)
    cwd = resolve_variables(lc.get("cwd", config.container_workspace), ctx)

    print(f"  Starting debugger: {command}")
    return exec_in_container(container, command, workdir=cwd, interactive=True)


def _run_go_remote(
    config: ProjectConfig, container: str, lc: dict, ctx: dict[str, str]
) -> int:
    """Run a Go remote debug configuration using dlv."""
    host = resolve_variables(lc.get("host", ""), ctx)
    port = lc.get("port", 4000)

    command = f"dlv connect {host}:{port}"
    print(f"  Starting debugger: {command}")
    return exec_in_container(
        container, command, workdir=config.container_workspace, interactive=True
    )


def list_launches(config: ProjectConfig) -> None:
    """Pretty-print all launch configurations."""
    launch_configs = load_launch_configs(config)
    if not launch_configs:
        print("No launch configurations found.")
        return

    print(f"Launch configurations ({len(launch_configs)}):\n")
    for lc in launch_configs:
        name = lc.get("name", "<unnamed>")
        lc_type = lc.get("type", "")
        mode = lc.get("mode", lc.get("request", ""))
        pre_task = lc.get("preLaunchTask", "")

        line = f"  {name}  [{lc_type}]"
        if mode:
            line += f"  ({mode})"
        if pre_task:
            line += f"  pre: {pre_task}"
        print(line)

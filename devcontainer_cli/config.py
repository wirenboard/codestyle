"""Configuration parsing for devcontainer-cli.

Parses devcontainer.json, tasks.json, launch.json with JSONC support
and VS Code variable resolution.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# Russian placeholder → ASCII key mapping
PLACEHOLDER_MAP = {
    "ИМЯ ПРОЕКТА": "PROJECT_NAME",
    "ИМЯ БИНАРНИКА": "BINARY_NAME",
    "IP КОНТРОЛЛЕРА": "CONTROLLER_IP",
    "ПАПКА С БИНАРНИКОМ ТЕСТОВ": "TEST_BINARY_DIR",
    "ИМЯ БИНАРНИКА ТЕСТОВ": "TEST_BINARY_NAME",
    "ИМЯ ТЕСТА": "TEST_FILTER",
}

# Reverse mapping for display
ASCII_TO_RUSSIAN = {v: k for k, v in PLACEHOLDER_MAP.items()}

PLACEHOLDER_DESCRIPTIONS = {
    "PROJECT_NAME": "Project name (basename of project dir)",
    "BINARY_NAME": "Binary name to build/deploy",
    "CONTROLLER_IP": "IP address of the target controller",
    "TEST_BINARY_DIR": "Directory containing test binary",
    "TEST_BINARY_NAME": "Test binary name",
    "TEST_FILTER": "Test filter (e.g. gtest_filter pattern)",
}


def load_jsonc(path: str) -> dict:
    """Load a JSONC file (JSON with comments and trailing commas)."""
    text = Path(path).read_text(encoding="utf-8")
    # Remove single-line comments (// ...) but not inside strings
    result = []
    in_string = False
    escape = False
    i = 0
    while i < len(text):
        ch = text[i]
        if escape:
            result.append(ch)
            escape = False
            i += 1
            continue
        if ch == "\\" and in_string:
            result.append(ch)
            escape = True
            i += 1
            continue
        if ch == '"' and not escape:
            in_string = not in_string
            result.append(ch)
            i += 1
            continue
        if not in_string and ch == "/" and i + 1 < len(text):
            if text[i + 1] == "/":
                # Skip single-line comment until end of line
                while i < len(text) and text[i] != "\n":
                    i += 1
                continue
            if text[i + 1] == "*":
                # Skip block comment until */
                i += 2
                while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                    i += 1
                i += 2  # skip closing */
                continue
        result.append(ch)
        i += 1
    text = "".join(result)
    # Remove trailing commas before } or ]
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return json.loads(text)


@dataclass
class DevcontainerConfig:
    image: str = ""
    run_args: list[str] = field(default_factory=list)
    mounts: list[dict[str, str]] = field(default_factory=list)
    post_create_command: str = ""
    container_env: dict[str, str] = field(default_factory=dict)


def parse_mount_spec(mount_string: str, variables: dict[str, str]) -> dict[str, str]:
    """Parse a mount specification string into a dict.

    Input: "source=${localWorkspaceFolder}/../codestyle,target=/workspaces/codestyle,type=bind"
    Output: {"source": "/resolved/path", "target": "/workspaces/codestyle", "type": "bind"}
    """
    mount = {}
    for part in mount_string.split(","):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        value = resolve_variables(value, variables)
        # Normalize source paths (resolve .. components)
        if key == "source":
            value = str(Path(value).resolve())
        mount[key] = value
    return mount


def parse_devcontainer(path: str, variables: dict[str, str]) -> DevcontainerConfig:
    """Parse a devcontainer.json file."""
    data = load_jsonc(path)
    config = DevcontainerConfig()
    config.image = data.get("image", "")
    config.run_args = data.get("runArgs", [])

    raw_mounts = data.get("mounts", [])
    for m in raw_mounts:
        if isinstance(m, str):
            config.mounts.append(parse_mount_spec(m, variables))
        elif isinstance(m, dict):
            resolved = {}
            for k, v in m.items():
                resolved[k] = resolve_variables(str(v), variables)
            config.mounts.append(resolved)

    config.post_create_command = data.get("postCreateCommand", "")
    raw_env = data.get("containerEnv", {})
    for k, v in raw_env.items():
        config.container_env[k] = resolve_variables(v, variables)

    return config


def resolve_variables(text: str, context: dict[str, str]) -> str:
    """Resolve VS Code variables and Russian placeholders in text.

    Handles:
      ${localWorkspaceFolder}  → context["localWorkspaceFolder"]
      ${workspaceFolder}       → context["workspaceFolder"]
      ${workspaceRoot}         → context["workspaceFolder"]
      ${localEnv:VARNAME}      → os.environ.get(VARNAME, "")
      <RUSSIAN PLACEHOLDER>    → context value via PLACEHOLDER_MAP
    """
    if not isinstance(text, str):
        return text

    # Resolve ${localEnv:VARNAME}
    def replace_local_env(m: re.Match[str]) -> str:
        var_name = m.group(1)
        return os.environ.get(var_name, "")

    text = re.sub(r"\$\{localEnv:([^}]+)\}", replace_local_env, text)

    # Resolve ${variable} patterns
    def replace_var(m: re.Match[str]) -> str:
        var_name = m.group(1)
        if var_name == "workspaceRoot":
            var_name = "workspaceFolder"
        return context.get(var_name, m.group(0))

    text = re.sub(r"\$\{([^}:]+)\}", replace_var, text)

    # Resolve Russian placeholders: <ИМЯ ПРОЕКТА> → context value
    for russian, ascii_key in PLACEHOLDER_MAP.items():
        placeholder = f"<{russian}>"
        if placeholder in text and ascii_key in context:
            text = text.replace(placeholder, context[ascii_key])

    return text


def detect_language(project_dir: str) -> str | None:
    """Auto-detect language from project's devcontainer.json."""
    devcontainer_path = os.path.join(project_dir, ".devcontainer", "devcontainer.json")
    if not os.path.exists(devcontainer_path):
        return None
    try:
        data = load_jsonc(devcontainer_path)
    except (json.JSONDecodeError, OSError):
        return None
    post_create = data.get("postCreateCommand", "")
    if "cpp/" in post_create:
        return "cpp"
    if "go/" in post_create:
        return "go"
    if "python/" in post_create:
        return "python"
    return None


def extract_vars_from_makefile(project_dir: str) -> dict[str, str]:
    """Try to extract BINARY_NAME, TEST_BINARY_NAME, TEST_BINARY_DIR from Makefile."""
    makefile_path = os.path.join(project_dir, "Makefile")
    if not os.path.exists(makefile_path):
        return {}

    try:
        text = Path(makefile_path).read_text(encoding="utf-8")
    except OSError:
        return {}

    result: dict[str, str] = {}

    # Patterns for the main binary name.
    # Match lines like: SERIAL_BIN = wb-mqtt-serial
    #                   BIN = my-daemon
    #                   BINARY_NAME = foo
    # Only match simple assignments (no $(shell ...) or $(...) references).
    for pattern in [
        r"^(?:SERIAL_BIN|BIN_NAME|BIN|BINARY)\s*[:?]?=\s*(\S+)",
    ]:
        m = re.search(pattern, text, re.MULTILINE)
        if m:
            value = m.group(1)
            if "$" not in value:
                result.setdefault("BINARY_NAME", value)
                break

    # Test binary name: TEST_BIN = wb-homa-test
    for pattern in [
        r"^TEST_BIN\s*[:?]?=\s*(\S+)",
    ]:
        m = re.search(pattern, text, re.MULTILINE)
        if m:
            value = m.group(1)
            if "$" not in value:
                result.setdefault("TEST_BINARY_NAME", value)
                break

    # Test directory: TEST_DIR = test
    for pattern in [
        r"^TEST_DIR\s*[:?]?=\s*(\S+)",
    ]:
        m = re.search(pattern, text, re.MULTILINE)
        if m:
            value = m.group(1)
            if "$" not in value:
                result.setdefault("TEST_BINARY_DIR", value)
                break

    return result


def load_user_vars(project_dir: str) -> dict[str, str]:
    """Load user variables from .devcontainer-cli.json in project dir."""
    vars_path = os.path.join(project_dir, ".devcontainer-cli.json")
    if not os.path.exists(vars_path):
        return {}
    try:
        with open(vars_path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print(f"Warning: {vars_path} should contain a JSON object", file=sys.stderr)
            return {}
        return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: failed to load {vars_path}: {e}", file=sys.stderr)
        return {}


def find_unresolved_placeholders(text: str) -> list[str]:
    """Find Russian placeholders that haven't been resolved yet."""
    found = []
    for russian in PLACEHOLDER_MAP:
        if f"<{russian}>" in text:
            ascii_key = PLACEHOLDER_MAP[russian]
            if ascii_key not in found:
                found.append(ascii_key)
    return found


def prompt_for_variables(needed: list[str], user_vars: dict[str, str]) -> dict[str, str]:
    """Interactively prompt for unresolved variables."""
    for var in needed:
        if var in user_vars:
            continue
        russian = ASCII_TO_RUSSIAN.get(var, var)
        desc = PLACEHOLDER_DESCRIPTIONS.get(var, var)
        if var == "PROJECT_NAME":
            # Don't prompt for PROJECT_NAME, it's auto-set
            continue
        try:
            value = input(f"  {var} ({desc}) [<{russian}>]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            value = ""
        if value:
            user_vars[var] = value
    return user_vars


@dataclass
class ProjectConfig:
    project_dir: str = ""
    codestyle_dir: str = ""
    language: str = ""
    devcontainer: DevcontainerConfig = field(default_factory=DevcontainerConfig)
    user_vars: dict[str, str] = field(default_factory=dict)

    @property
    def project_name(self) -> str:
        return os.path.basename(self.project_dir)

    @property
    def container_workspace(self) -> str:
        return f"/workspaces/{self.project_name}"

    def vscode_dir(self) -> str:
        """Path to the language-specific .vscode directory in codestyle."""
        return os.path.join(self.codestyle_dir, self.language, "vscode", ".vscode")

    def make_variable_context(self) -> dict[str, str]:
        """Build the full variable context for resolution."""
        ctx = {
            "localWorkspaceFolder": self.project_dir,
            "workspaceFolder": self.container_workspace,
            "PROJECT_NAME": self.project_name,
        }
        ctx.update(self.user_vars)
        return ctx


def build_config(
    project_dir: str,
    codestyle_dir: str,
    language: str | None = None,
    cli_vars: dict[str, str] | None = None,
) -> ProjectConfig:
    """Build a complete ProjectConfig from arguments."""
    project_dir = os.path.abspath(project_dir)
    codestyle_dir = os.path.abspath(codestyle_dir)

    if not os.path.isdir(project_dir):
        print(f"Error: project directory not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(codestyle_dir):
        print(f"Error: codestyle directory not found: {codestyle_dir}", file=sys.stderr)
        sys.exit(1)

    if language is None:
        language = detect_language(project_dir)
        if language is None:
            print(
                "Error: cannot auto-detect language. Use --language cpp|go|python",
                file=sys.stderr,
            )
            sys.exit(1)

    devcontainer_path = os.path.join(
        codestyle_dir, language, "vscode", ".devcontainer", "devcontainer.json"
    )
    if not os.path.exists(devcontainer_path):
        print(f"Error: devcontainer.json not found: {devcontainer_path}", file=sys.stderr)
        sys.exit(1)

    # Merge variable sources: CLI vars > .devcontainer-cli.json > Makefile > defaults
    makefile_vars = extract_vars_from_makefile(project_dir)
    user_vars = makefile_vars
    user_vars.update(load_user_vars(project_dir))
    if cli_vars:
        user_vars.update(cli_vars)
    # Always set PROJECT_NAME
    user_vars.setdefault("PROJECT_NAME", os.path.basename(project_dir))

    config = ProjectConfig(
        project_dir=project_dir,
        codestyle_dir=codestyle_dir,
        language=language,
        user_vars=user_vars,
    )

    variables = config.make_variable_context()
    config.devcontainer = parse_devcontainer(devcontainer_path, variables)

    return config

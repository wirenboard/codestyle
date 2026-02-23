# devcontainer-cli

VS Code DevContainers without VS Code. Runs the same `devcontainer.json`, `tasks.json`, and `launch.json` configs from the codestyle repo via CLI.

## Quick Start

```bash
cd ~/work/board/wb-mqtt-serial
../codestyle/devcontainer-cli up --language cpp
```

This creates a Docker container, starts it, and runs `postCreateCommand` (installs dev dependencies).

## Commands

### Container Lifecycle

```bash
# Create and start container (first time runs postCreateCommand)
../codestyle/devcontainer-cli up --language cpp

# Rebuild from scratch
../codestyle/devcontainer-cli up --language cpp --rebuild

# Stop container (keeps state)
../codestyle/devcontainer-cli stop

# Start stopped container
../codestyle/devcontainer-cli start

# Stop and remove container
../codestyle/devcontainer-cli down

# Show container state
../codestyle/devcontainer-cli status
```

### Saving & Loading Containers

After `up` runs `postCreateCommand` (which can take several minutes), you can snapshot the container to a file and restore it later — skipping the slow setup entirely.

```bash
# Save the prepared container to a tar.gz file
../codestyle/devcontainer-cli save
# Creates cpp-devenv.tar.gz (default name based on language)

# Save with a custom filename
../codestyle/devcontainer-cli save my-snapshot.tar.gz

# Create a new container from the saved file (fast, no postCreateCommand)
../codestyle/devcontainer-cli down
../codestyle/devcontainer-cli up --image cpp-devenv.tar.gz
```

`--image` accepts both tar.gz files and Docker image tags. When given a file, it loads the image automatically.

This is useful for sharing pre-built environments with teammates or moving them between machines.

### Run Commands in Container

```bash
# Run arbitrary command
../codestyle/devcontainer-cli exec ls -la

# Run tests via qemu
../codestyle/devcontainer-cli exec 'cd test && qemu-arm-static -L /srv/chroot/sbuild-bullseye-cross wb-homa-test'
```

### Tasks (from tasks.json)

```bash
# List all available tasks
../codestyle/devcontainer-cli tasks list

# Build for armhf
../codestyle/devcontainer-cli tasks run "[armhf] Build"

# Build for arm64
../codestyle/devcontainer-cli tasks run "[arm64] Build"

# Debug build
../codestyle/devcontainer-cli tasks run "[armhf] Debug build"

# Run all tests
../codestyle/devcontainer-cli tasks run "[armhf] Run all tests"

# Build and copy to controller (BINARY_NAME from Makefile, prompts for CONTROLLER_IP)
../codestyle/devcontainer-cli tasks run "[armhf] Build and copy to remote target"

# Same, with CONTROLLER_IP pre-set
../codestyle/devcontainer-cli \
  --var CONTROLLER_IP=192.168.1.100 \
  tasks run "[armhf] Build and copy to remote target"
```

### Launch/Debug Configs (from launch.json)

```bash
# List available debug configurations
../codestyle/devcontainer-cli launch list

# Remote debug (BINARY_NAME from Makefile, only need CONTROLLER_IP)
../codestyle/devcontainer-cli \
  --var CONTROLLER_IP=192.168.1.100 \
  launch run "[armhf] Remote debug"

# Debug tests locally via qemu (all variables auto-detected from Makefile)
../codestyle/devcontainer-cli launch run "[armhf] Debug tests"
```

## Variables

Tasks and launch configs use placeholder variables (shown as `<ИМЯ ПРОЕКТА>` etc. in VS Code configs). Resolved from these sources (highest priority first):

1. `--var KEY=VALUE` flags
2. `.devcontainer-cli.json` in project root
3. **Makefile auto-extraction** (parses `SERIAL_BIN`, `TEST_BIN`, `TEST_DIR`)
4. Interactive prompt (if still unresolved)

For wb-mqtt-serial, the Makefile contains `SERIAL_BIN = wb-mqtt-serial`, `TEST_BIN = wb-homa-test`, `TEST_DIR = test`, so `BINARY_NAME`, `TEST_BINARY_NAME`, and `TEST_BINARY_DIR` are set automatically — no `--var` flags needed.

| Variable | Description | Auto-detected from Makefile |
|----------|-------------|-----------------------------|
| `PROJECT_NAME` | Project name | Always (directory name) |
| `BINARY_NAME` | Binary to build/deploy | `SERIAL_BIN`, `BIN_NAME`, `BIN`, `BINARY` |
| `TEST_BINARY_NAME` | Test binary name | `TEST_BIN` |
| `TEST_BINARY_DIR` | Test binary directory | `TEST_DIR` |
| `CONTROLLER_IP` | Target controller IP | No (must be set manually) |
| `TEST_FILTER` | gtest filter pattern | No (must be set manually) |

Example `.devcontainer-cli.json` (only needed for variables that can't be auto-detected):

```json
{
  "CONTROLLER_IP": "192.168.1.100"
}
```

## Global Options

```
--project-dir DIR         Project directory (default: current directory)
--codestyle-dir DIR       Path to codestyle repo (default: auto-detected)
--language cpp|go|python  Language config (default: auto-detect from devcontainer.json)
--var KEY=VALUE           Set a variable (repeatable)
```

## Language Auto-Detection

If the project has `.devcontainer/devcontainer.json` with a `postCreateCommand` referencing `cpp/`, `go/`, or `python/`, the language is detected automatically. Otherwise, use `--language`.

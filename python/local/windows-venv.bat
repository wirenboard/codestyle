@echo off

copy "..\codestyle\python\config\pyproject.toml" "."
pip install virtualenv
python -m venv .venv
call ".venv\Scripts\activate.bat"
pip install -r "..\codestyle\python\config\requirements.txt"
pip install attrs==23.1.0  

REM don't want to make windows code complicated, so just copy extensions from .devcontainer.json
set extensions=ms-python.python ms-python.pylint@2024.2.0 ms-python.black-formatter@2024.6.0 ms-python.isort@2025.0.0

for %%e in (%extensions%) do (
    echo %%e | find "@" >nul
    if errorlevel 1 (
        code --list-extensions | find "%%e" >nul
        if errorlevel 1 (
            code --install-extension "%%e"
        ) else (
            echo Extension %%e is already installed
        )
    ) else (
        for /f "tokens=1,2 delims=@" %%a in ("%%e") do (
            code --list-extensions --show-versions | find "%%a@%%b" >nul
            if errorlevel 1 (
                code --install-extension "%%e" --force
            ) else (
                echo Extension %%e is already installed
            )
        )
    )
)
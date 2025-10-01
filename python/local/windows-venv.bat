copy "..\codestyle\python\config\pyproject.toml" "."
pip install virtualenv
python -m venv .venv
call ".venv\Scripts\activate.bat"
pip install -r "..\codestyle\python\config\requirements.txt"
pip install attrs==23.1.0  

set extensions=
for /f "tokens=*" %%i in ('python -c "import json; data=json.load(open('..\codestyle\python\\vscode\.devcontainer\devcontainer.json')); print(' '.join([ext for ext in data['customizations']['vscode']['extensions'] if ext.startswith('ms-python')]))"') do set extensions=%%i

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
  @echo off
)
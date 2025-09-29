@echo off

copy "..\codestyle\python\config\pyproject.toml" "."
copy "..\codestyle\python\config\.coveragerc" "."
python -m venv .venv
call ".venv\Scripts\activate.bat"
pip install -r "..\codestyle\python\config\requirements.txt"
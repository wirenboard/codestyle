#!/bin/bash
cp ../codestyle/python/config/pyproject.toml ./
pip3 install virtualenv
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r ../codestyle/python/config/requirements.txt
pip3 install attrs==23.1.0 # fix isort deps

#get only python extensions from devcontainer.json
extensions=$(jq -r '.customizations.vscode.extensions[]' ../codestyle/python/vscode/.devcontainer/devcontainer.json | grep '^ms-python')

for extension in $extensions; do
    if [[ "$extension" == *"@"* ]]; then
        extension_name=$(echo "$extension" | cut -d'@' -f1)
        extension_version=$(echo "$extension" | cut -d'@' -f2)
        
        if code --list-extensions --show-versions | grep -q "^$extension_name@$extension_version$"; then
            echo "Extension $extension is already installed"
        else
            code --install-extension "$extension" --force
        fi
    else
        if code --list-extensions | grep -q "^$extension$"; then
            echo "Extension $extension is already installed"
        else
            code --install-extension "$extension" 
        fi
    fi
done

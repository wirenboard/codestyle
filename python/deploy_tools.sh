#!/bin/bash

set -e

PYLINTRC_URL=https://raw.githubusercontent.com/wirenboard/codestyle/master/python/pylintrc
PYPROJECT_URL=https://raw.githubusercontent.com/wirenboard/codestyle/master/python/pyproject.toml
REQUIREMENTS_URL=https://raw.githubusercontent.com/wirenboard/codestyle/master/python/requirements.txt
VENV_NAME=codestyle_venv

DEPLOY_DIR="${DEPLOY_DIR:-/home/$USER/.config/wb}"

pushd $DEPLOY_DIR
wget $PYLINTRC_URL -O pylintrc
wget $PYPROJECT_URL -O pyproject.toml
# wget $REQUIREMENTS_URL -O requirements.txt
python3 -m venv $VENV_NAME
source $VENV_NAME/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt; deactivate $VENV_NAME
popd
#!/bin/env bash

set -e

PYLINTRC_URL=https://raw.githubusercontent.com/wirenboard/codestyle/master/python/pylintrc
PYPROJECT_URL=https://raw.githubusercontent.com/wirenboard/codestyle/master/python/pyproject.toml
REQUIREMENTS_URL=https://raw.githubusercontent.com/wirenboard/codestyle/feature/python-tools/python/requirements.txt

DEPLOY_DIR="${DEPLOY_DIR:-/home/$USER/.config/wb}"
VENV="${VENV:-$DEPLOY_DIR/codestyle_venv}"

mkdir -p $DEPLOY_DIR
pushd $DEPLOY_DIR
if [[ -z "$SKIP_DOWNLOAD_CONFIGS" ]]; then
    wget $PYLINTRC_URL -O pylintrc
    wget $PYPROJECT_URL -O pyproject.toml
    wget $REQUIREMENTS_URL -O requirements.txt
fi
popd
python3 -m venv $VENV
source $VENV/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r $DEPLOY_DIR/requirements.txt; deactivate $VENV

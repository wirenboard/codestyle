#!/bin/bash

cp ../codestyle/python/config/pyproject.toml ./
cp ../codestyle/python/config/.coveragerc ./
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r ../codestyle/python/config/requirements.txt
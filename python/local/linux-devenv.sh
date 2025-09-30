#!/bin/bash
cp ../codestyle/python/config/pyproject.toml ./
cp ../codestyle/python/config/.coveragerc ./
pip3 install -r ../codestyle/python/config/requirements.txt
pip3 install attrs==23.1.0 # fix isort deps
apt update
mk-build-deps -ir -t 'apt-get --force-yes -y'
find ./ -name '*.changes' -delete
find ./ -name '*.buildinfo' -delete
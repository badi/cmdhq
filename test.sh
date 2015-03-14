#!/usr/bin/env bash

set -o errexit

export CMDHQ_PLUGINS_PATH=$PWD/plugins:$PWD/plugins2

# the following is intended to fail
set +e
python cmdhq/__init__.py foo
set -e

python cmdhq/__init__.py hello
python cmdhq/__init__.py foo.bar
python cmdhq/__init__.py plugins2



#!/bin/sh
# Script which installs the pipxu program from PyPi to a temporary
# Python virtual environment where pipxu is then run to install itself
# again normally.
# M.Blakeney, Feb 2024.
trap 'rm -rf $VENV' EXIT
VENV=$(mktemp -d)
python3 -m venv $VENV
$VENV/bin/pip install pipxu
$VENV/bin/pipxu install -f pipxu

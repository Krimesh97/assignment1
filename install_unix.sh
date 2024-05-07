#!/bin/bash
echo "Installing dependencies..."
python3 -m pip install virtualenv
python3 -m virtualenv ./.venv --python=3.11
source ./.venv/bin/activate
python3 -m pip install -r requirements.txt
echo "Dependencies installed successfully."
source deactivate


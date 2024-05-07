#!/usr/bin/env bash
set -e
source ./.venv/bin/activate
python ./main.py
source deactivate
read -p "Press enter to continue"

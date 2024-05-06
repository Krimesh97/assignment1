#!/bin/bash
echo "Installing dependencies..."
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Dependencies installed successfully."


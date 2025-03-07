#!/bin/bash

echo "Running as user $(whoami)"
# Add /video2x to PATH
export PATH=$PATH:/video2x
video2x -l
# Create and activate virtual environment
python3 -m venv ~/video2x-venv/
source ~/video2x-venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r /scripts/requirements.txt
echo "Starting process"
python3 -u /scripts/process.py
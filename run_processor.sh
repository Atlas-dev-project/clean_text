#!/bin/bash

# Read the base_dir from config.py
BASE_DIR=$(python3 -c "import config; print(config.base_dir)")

# Set the BASE_DIR environment variable
export BASE_DIR

# Set the PYTHONPATH to the current directory
export PYTHONPATH=$(pwd)

# Activate the virtual environment
source venv/bin/activate

# Install dependencies if not already installed
pip install -r requirements.txt

# Run the main script
python3 main.py

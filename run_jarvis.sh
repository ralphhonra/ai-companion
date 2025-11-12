#!/bin/bash

# Quick launcher for JARVIS
# This activates the virtual environment and runs JARVIS

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run ./setup.sh first to install dependencies."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run JARVIS with any arguments passed to this script
python jarvis.py "$@"


#!/bin/bash
set -e

# Use Python 3.11 (assumes pyenv or system Python 3.11 is installed)
# If using GitHub Actions, this is handled by actions/setup-python

echo "Using Python version:"
python3 --version

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
pip install pytest

# Export PYTHONPATH to include current directory (project root)
export PYTHONPATH=$(pwd)

# Run tests
pytest tests/
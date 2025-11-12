#!/bin/bash
set -e

# Check if pyenv is installed and Python 3.11 is available
if command -v pyenv >/dev/null 2>&1; then
  echo "pyenv detected. Installing and using Python 3.11.0"
  pyenv install -s 3.11.0
  pyenv local 3.11.0
else
  echo "pyenv not found. Assuming system Python 3.11 is installed."
fi

echo "Using Python version:"
python3 --version

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
pip install pytest

# Set PYTHONPATH to current directory (project root)
export PYTHONPATH=$(pwd)

# Run tests
pytest tests/
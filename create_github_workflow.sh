#!/bin/bash
set -e

cat > .github/workflows/python-tests.yml << 'EOF'
name: Python Tests

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        python -m venv .venv
        source .venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests with PYTHONPATH
      env:
        PYTHONPATH: ${{ github.workspace }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        source .venv/bin/activate
        pytest tests/
EOF

echo "GitHub Actions workflow file created at .github/workflows/python-tests.yml"
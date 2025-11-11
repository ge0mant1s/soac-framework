#!/bin/bash

# Variables
WORKFLOW_DIR=".github/workflows"
WORKFLOW_FILE="python-tests.yml"
REPO_BRANCH="main"  # Change if your default branch is different

# Create workflow directory if it doesn't exist
mkdir -p "$WORKFLOW_DIR"

# Write the GitHub Actions workflow YAML
cat > "$WORKFLOW_DIR/$WORKFLOW_FILE" << 'EOF'
name: Python Tests

on:
  push:
    branches:
      - main
      - master
      - '**'
  pull_request:
    branches:
      - main
      - master

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python 3.14
      uses: actions/setup-python@v4
      with:
        python-version: 3.14

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest

    - name: Run tests
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        ABACUS_API_KEY: ${{ secrets.ABACUS_API_KEY }}
      run: |
        PYTHONPATH=$(pwd) pytest tests/
EOF

# Add, commit, and push the workflow file
git add "$WORKFLOW_DIR/$WORKFLOW_FILE"
git commit -m "Add GitHub Actions workflow for running Python tests"
git push origin "$REPO_BRANCH"

echo "GitHub Actions workflow deployed and pushed to branch $REPO_BRANCH."
echo "Make sure to add OPENAI_API_KEY and ABACUS_API_KEY as secrets in your GitHub repository settings."
#!/bin/bash

# Create directories if they don't exist
mkdir -p .github/workflows

# Write the updated workflow to ci.yml
cat > .github/workflows/ci.yml << 'EOF'
name: Python Tests

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Upgrade pip
        run: python -m pip install --upgrade pip

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Run tests
        run: pytest
EOF

# Add, commit, and push changes
git add .github/workflows/ci.yml
git commit -m "Update GitHub Actions workflow to use Python 3.11 for compatibility"
git push origin main
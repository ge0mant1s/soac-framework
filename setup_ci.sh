#!/bin/bash

# Create directories if they don't exist
mkdir -p .github/workflows
mkdir -p api

# Create GitHub Actions workflow file
cat > .github/workflows/ci.yml << 'EOF'
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: soac
          POSTGRES_USER: soac
          POSTGRES_PASSWORD: soac123
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r api/requirements.txt
          pip install pytest

      - name: Wait for Postgres
        run: |
          until pg_isready -h localhost -p 5432; do
            echo "Waiting for Postgres..."
            sleep 2
          done

      - name: Run tests
        env:
          DB_HOST: localhost
          DB_NAME: soac
          DB_USER: soac
          DB_PASSWORD: soac123
        run: pytest tests/
EOF

# Update api/requirements.txt with the required packages
cat > api/requirements.txt << 'EOF'
openai
flask
flask-cors
psycopg2-binary
pytest
EOF

echo "✅ GitHub Actions workflow and requirements.txt updated successfully."

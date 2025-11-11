#!/bin/bash

# Create tests directory if it doesn't exist
mkdir -p tests

# Create a simple test file
cat > tests/test_sample.py << 'EOF'
def test_example():
    assert 1 + 1 == 2
EOF

echo "Created tests/test_sample.py with a simple test."

# Path to your GitHub Actions workflow file
WORKFLOW_FILE=".github/workflows/python-tests.yml"

# Check if workflow file exists
if [ ! -f "$WORKFLOW_FILE" ]; then
  echo "Workflow file $WORKFLOW_FILE not found. Please check the path."
  exit 1
fi

# Update the workflow file to run pytest on tests/ folder
# This replaces any line starting with 'run: pytest' with 'run: pytest tests/'

sed -i.bak -E 's|run: pytest.*|run: pytest tests/|' "$WORKFLOW_FILE"

echo "Updated $WORKFLOW_FILE to run 'pytest tests/'"

echo "Done. Please commit and push these changes."
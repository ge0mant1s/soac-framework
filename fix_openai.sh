#!/bin/bash
set -e

# File to patch
FILE="ai_engine/openai_assistant.py"

echo "Patching $FILE for OpenAI SDK v1.6.1 compatibility..."

# Backup original file
cp "$FILE" "${FILE}.bak"

# Replace the __init__ method to remove proxies and set api_key globally
sed -i.bak -E '/def __init__\(self\):/,/self.client = openai.OpenAI\(.*\)/c\
def __init__(self):\
    import os\
    self.api_key = os.getenv("OPENAI_API_KEY")\
    import openai\
    openai.api_key = self.api_key\
    self.client = openai.OpenAI()' "$FILE"

echo "Patch applied."

# Activate virtual environment
source .venv/bin/activate

# Run tests
echo "Running tests..."
pytest tests/

echo "Done."
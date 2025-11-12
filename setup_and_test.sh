#!/bin/bash

# Navigate to your project directory
cd /Users/geo/GitHub || exit 1

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  echo "Created virtual environment in .venv"
fi

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install OpenAI package
pip install openai

# Verify installation
pip show openai

# Run a test Python command to check OpenAIAssistant
python -c "from ai_engine.openai_assistant import OpenAIAssistant; ai = OpenAIAssistant(); print(ai.summarize_incident('Example incident text'))"
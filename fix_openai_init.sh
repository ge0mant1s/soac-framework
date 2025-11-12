#!/bin/bash

# Find all Python files in your project
files=$(grep -rl "OpenAI(" . --include \*.py)

echo "Fixing OpenAI client initialization in files:"
echo "$files"

for file in $files; do
  echo "Processing $file"

  # Remove proxies argument from OpenAI() constructor calls
  # This handles cases like OpenAI(proxies=...) or OpenAI(proxies=..., api_key=...)
  sed -i.bak -E 's/OpenAI\(([^)]*)proxies=[^,)]*(,)?([^)]*)\)/OpenAI(\1\3)/g' "$file"

  # Remove api_key argument if present (optional, if you want to enforce env var usage)
  sed -i.bak -E 's/OpenAI\(([^)]*)api_key=[^,)]*(,)?([^)]*)\)/OpenAI(\1\3)/g' "$file"

  # Clean up any trailing commas left by removals
  sed -i.bak -E 's/OpenAI\(([^)]*),\)/OpenAI(\1)/g' "$file"

  # Remove backup file created by sed
  rm "${file}.bak"
done

echo "Fix complete. Please verify your code and tests."

#!/bin/bash
# SOaC Framework Setup Script

echo "========================================="
echo "SOaC Framework - Setup Script"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directory structure..."
mkdir -p logs
mkdir -p output
mkdir -p config

# Copy template config if config.json doesn't exist
if [ ! -f "config/config.json" ]; then
    echo ""
    echo "Creating default configuration..."
    cp config/config_template.json config/config.json
    echo "⚠️  Please edit config/config.json with your API credentials"
fi

# Run tests
echo ""
echo "Running tests..."
pytest tests/ -v

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Edit config/config.json with your API credentials"
echo "3. Run the framework: python app.py"
echo ""

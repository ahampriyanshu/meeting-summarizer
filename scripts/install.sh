#!/bin/bash
set -e

echo "📦 Installing dependencies for Meeting Summarizer Agent..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  - Set your OPENAI_API_KEY environment variable"
echo "  - Run 'bash scripts/run.sh' to start the Streamlit app"
echo "  - Run 'bash scripts/test.sh' to run the test suite"


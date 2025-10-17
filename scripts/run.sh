#!/bin/bash
set -e

echo "🚀 Starting Meeting Summarizer Agent..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY is not set"
    echo "Please set it with: export OPENAI_API_KEY='your-key-here'"
    echo ""
fi

# Run Streamlit app
streamlit run app.py --server.port 8501 --server.headless true


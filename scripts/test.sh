#!/bin/bash
set -e

echo "🧪 Running Meeting Summarizer Agent tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY is not set"
    echo "Please set it with: export OPENAI_API_KEY='your-key-here'"
    exit 1
fi

# Remove old test results
rm -f unit.xml

# Run pytest with JSON report
pytest tests/ -v --tb=short --json-report --json-report-file=unit.xml --json-report-indent=2

# Check if tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "❌ Some tests failed. Check the output above for details."
    exit 1
fi


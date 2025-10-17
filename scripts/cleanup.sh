#!/bin/bash

echo "🧹 Cleaning up Meeting Summarizer Agent..."

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Remove test artifacts
rm -f unit.xml 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true
rm -rf htmlcov 2>/dev/null || true
rm -f .coverage 2>/dev/null || true

# Remove virtual environment
rm -rf venv 2>/dev/null || true

echo "✅ Cleanup complete!"


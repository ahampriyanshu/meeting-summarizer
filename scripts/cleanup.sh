#!/bin/bash

echo "🧹 Cleaning workspace..."
rm -rf .pytest_cache/
rm -rf src/__pycache__/
rm -rf __pycache__/
rm -f unit.xml

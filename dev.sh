#!/bin/bash

# dev.sh - Development environment setup and launch script for ClaudeCart

set -e  # Exit on any error

echo "🛒 ClaudeCart Development Setup"
echo "================================"

# Clean up existing environment
echo "🧹 Cleaning up existing virtual environment..."
rm -rf .venv/

# Create new virtual environment
echo "🐍 Creating new virtual environment..."
uv venv

# Install dependencies
echo "📦 Installing dependencies..."
uv pip install -e .

# Activate virtual environment and run Streamlit
echo "🚀 Starting ClaudeCart..."
echo "   - Local URL: http://localhost:8501"
echo "   - Network URL will be shown below"
echo "   - Press Ctrl+C to stop"
echo ""

# Source the virtual environment and run streamlit
source .venv/bin/activate && streamlit run app.py
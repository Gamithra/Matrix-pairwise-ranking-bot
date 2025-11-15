#!/bin/bash
# Quick setup script for Matrix Pairwise Ranking Bot

echo "� Setting up Matrix Ranking Bot..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env with your Matrix credentials:"
    echo "   - MATRIX_HOMESERVER"
    echo "   - MATRIX_USER_ID"
    echo "   - MATRIX_PASSWORD"
    echo ""
    echo "Then run: ./run.sh"
else
    echo "✓ .env file exists"
fi

echo ""
echo "✅ Setup complete!"

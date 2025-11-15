#!/bin/bash
# Run the Matrix Pairwise Ranking Bot

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the bot with proper Python path
echo "� Starting Ranking Bot..."
export PYTHONPATH="$PWD/src:$PYTHONPATH"
cd src && python3 bot.py

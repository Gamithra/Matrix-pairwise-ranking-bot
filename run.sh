#!/bin/bash
# Run the Matrix pairwise ranking bot

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the bot with proper Python path
echo "Starting ranking bot..."
export PYTHONPATH="$PWD/src:$PYTHONPATH"
cd src && python3 bot.py

#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p output
mkdir -p logs

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it with your credentials."
fi

echo "Setup completed successfully."
echo "Next steps:"
echo "1. Edit the .env file with your email credentials"
echo "2. Run the tracker with: ./src/run.sh"
echo "3. Or set up the scheduler with: ./src/run_scheduler.sh"

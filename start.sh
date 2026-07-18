#!/bin/bash
# Quick Start Script for Campus Hub Portal

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         CAMPUS HUB PORTAL - QUICK START                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"
echo ""

# Check if database exists
if [ -f "campus_hub.db" ]; then
    echo "✓ Database already exists"
else
    echo "→ Initializing database..."
    python3 -c "from database import init_db; init_db()"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                 STARTING APPLICATION...                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Run the application
python3 main.py

#!/bin/bash
# Start script for Campus Hub Web Portal

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         CAMPUS HUB WEB PORTAL - STARTING SERVER         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "→ Flask not found. Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "✓ Flask is installed"

# Check if database exists
if [ -f "campus_hub.db" ]; then
    echo "✓ Database exists"
else
    echo "→ Initializing database..."
    python3 -c "from database import init_db; init_db()"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              SERVER STARTING ON PORT 5000                ║"
echo "║                                                          ║"
echo "║         Open your browser and navigate to:              ║"
echo "║              http://localhost:5000                       ║"
echo "║                                                          ║"
echo "║         Press Ctrl+C to stop the server                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Run the Flask application
python3 app.py

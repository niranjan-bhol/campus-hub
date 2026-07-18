#!/bin/bash
# Quick deployment script - Push to GitHub

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         CAMPUS HUB - DEPLOYMENT PREPARATION              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this from the campus-hub directory."
    exit 1
fi

echo "✅ Found app.py"
echo ""

# Show git status
echo "📊 Current Git Status:"
git status --short
echo ""

# Add all files
echo "➕ Adding deployment files..."
git add .

# Commit
echo ""
echo "💾 Committing changes..."
git commit -m "Add deployment configuration for Render/PythonAnywhere

- Add gunicorn to requirements.txt
- Add Procfile for Render/Railway
- Add render.yaml for automatic configuration
- Add runtime.txt for Python version
- Update app.py for production (env variables)
- Add deployment guides"

# Push
echo ""
echo "🚀 Pushing to GitHub..."
git push

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    ✅ SUCCESS!                           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Your code is now on GitHub and ready for deployment!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Go to: https://render.com"
echo "2. Sign up with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select your 'campus-hub' repository"
echo "5. Click 'Create Web Service'"
echo ""
echo "📖 Detailed instructions: RENDER_DEPLOY.md"
echo ""
echo "Your app will be live in 5-10 minutes! 🎉"
echo ""

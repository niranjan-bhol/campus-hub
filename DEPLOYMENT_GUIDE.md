# Campus Hub - Free Deployment Guide 🚀

## 🎯 Recommended Free Hosting Options

I'll guide you through **two best free options** for your Flask + SQLite app:

### Option 1: Render.com (⭐ Recommended)
- **Cost:** 100% Free
- **Pros:** Easy setup, automatic deploys from GitHub, HTTPS included
- **Cons:** SQLite data resets on redeploy (not ideal for production)
- **Best for:** Testing and small projects

### Option 2: PythonAnywhere
- **Cost:** Free tier available
- **Pros:** Python-specific, SQLite persistent, web console
- **Cons:** Custom domain only on paid plans
- **Best for:** Python apps with database persistence

---

## 🚀 Option 1: Deploy to Render.com (Easiest)

### Step 1: Prepare Your Repository

Your code is already on GitHub! ✅

### Step 2: Create Account on Render

1. Go to [https://render.com](https://render.com)
2. Click "Get Started" or "Sign Up"
3. Sign up with GitHub (recommended) or email
4. Verify your email

### Step 3: Create New Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Connect your GitHub account if not already connected
4. Select your `campus-hub` repository
5. Click "Connect"

### Step 4: Configure Service

Fill in these settings:

**Basic Settings:**
- **Name:** `campus-hub` (or your preferred name)
- **Region:** Choose closest to you
- **Branch:** `main` or `master`
- **Root Directory:** Leave blank
- **Runtime:** `Python 3`

**Build Settings:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Instance Type:**
- Select **"Free"** plan

### Step 5: Environment Variables (Optional)

Add these if needed:
- `PYTHON_VERSION`: `3.11.15`
- `SECRET_KEY`: (generate a random string)

### Step 6: Deploy!

1. Click "Create Web Service"
2. Wait 5-10 minutes for first deploy
3. Your app will be live at: `https://campus-hub.onrender.com`

### Step 7: Access Your App

Once deployment succeeds, click the URL at top of dashboard!

**⚠️ Important Note about SQLite on Render:**
- Database resets when app redeploys or sleeps
- For production, consider upgrading to PostgreSQL (still free on Render)
- Good for testing/demo purposes

---

## 🐍 Option 2: Deploy to PythonAnywhere

### Step 1: Create Account

1. Go to [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Click "Pricing & signup"
3. Select "Create a Beginner account" (Free)
4. Fill in username, email, password
5. Verify email

### Step 2: Upload Your Code

**Option A: From GitHub (Recommended)**

Open a Bash console in PythonAnywhere:
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/campus-hub.git
cd campus-hub
```

**Option B: Upload Files**
- Use "Files" tab to upload your project files

### Step 3: Set Up Virtual Environment

In the Bash console:
```bash
cd ~/campus-hub
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select "Python 3.11"

### Step 5: Configure WSGI File

1. In "Web" tab, find "WSGI configuration file" link
2. Click it to edit
3. Replace ALL content with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/campus-hub'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variable for Flask
os.environ['FLASK_APP'] = 'app.py'

# Import Flask app
from app import app as application
```

Replace `YOUR_USERNAME` with your PythonAnywhere username.

### Step 6: Set Virtual Environment

In "Web" tab:
1. Find "Virtualenv" section
2. Enter: `/home/YOUR_USERNAME/campus-hub/venv`

### Step 7: Initialize Database

In Bash console:
```bash
cd ~/campus-hub
source venv/bin/activate
python -c "from database import init_db; init_db()"
```

### Step 8: Reload and Launch

1. Click green "Reload" button in Web tab
2. Your app is live at: `https://YOUR_USERNAME.pythonanywhere.com`

**✅ PythonAnywhere Advantages:**
- SQLite database persists between restarts
- Free SSL certificate included
- Python-optimized environment

---

## 🔧 Alternative Options

### Option 3: Railway.app
- Free $5/month credit
- GitHub integration
- Good for Flask apps
- **Setup:** Similar to Render

### Option 4: Fly.io
- Free tier available
- Good performance
- Requires Docker knowledge
- **Complexity:** Medium

---

## ⚠️ Important Considerations

### Database Persistence

**SQLite on Free Hosting:**
- **Render:** Database resets on redeploy ❌
- **PythonAnywhere:** Database persists ✅
- **Railway:** Database persists ✅

**For Production Use:**
Consider switching to PostgreSQL (still free on Render/Railway).

### Free Tier Limitations

**Render Free Tier:**
- App sleeps after 15 minutes of inactivity
- Cold start takes 30-60 seconds
- 750 hours/month (basically unlimited for one app)

**PythonAnywhere Free Tier:**
- Always on (no sleep)
- Limited CPU/bandwidth
- HTTP only (HTTPS requires paid plan)

**Railway Free Tier:**
- $5 credit per month
- Good for small apps
- 500 hours execution time

---

## 🎯 My Recommendation

**For Demo/Testing:**
→ Use **Render.com** (easiest setup, looks professional)

**For Actual Campus Use:**
→ Use **PythonAnywhere** (database persists, always on)

**For Best Performance:**
→ Use **Railway.app** (fast, reliable, $5 credit/month)

---

## 🔗 Useful Links

- **Render:** https://render.com
- **PythonAnywhere:** https://www.pythonanywhere.com
- **Railway:** https://railway.app
- **Fly.io:** https://fly.io

---

## 📞 Need Help?

If you choose Render, I can help you:
1. ✅ Create production config files
2. ✅ Set up PostgreSQL (still free!)
3. ✅ Configure environment variables
4. ✅ Optimize for deployment

If you choose PythonAnywhere, I can help you:
1. ✅ Configure WSGI properly
2. ✅ Set up static files
3. ✅ Debug any deployment issues

**Let me know which option you'd like to use, and I'll help you through it!** 🚀

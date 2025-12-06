# PythonAnywhere Deployment Guide

## 📋 Pre-Deployment Checklist

✅ **Completed:**
- ✅ `requirements.txt` created with all dependencies
- ✅ `wsgi.py` WSGI configuration file created
- ✅ `app.py` updated with `debug=False` for production
- ✅ All templates in `templates/` folder
- ✅ All static files in `static/` folder
- ✅ Uploads directory will be created automatically

## 🚀 Step-by-Step Deployment on PythonAnywhere

### Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com
2. Create a free or paid account
3. Log in to your dashboard

### Step 2: Upload Files
1. In PythonAnywhere Dashboard, go to **Files**
2. Create a new directory: `/home/yourusername/level30app/`
3. Upload the following files and folders:
   - `app.py`
   - `wsgi.py`
   - `requirements.txt`
   - `templates/` (entire folder with all .html files)
   - `static/` (entire folder with CSS, images, and uploads subfolder)

### Step 3: Create Virtual Environment
1. Go to **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10** (or latest available)
5. In **Virtualenv**, enter: `/home/yourusername/.virtualenvs/level30`

### Step 4: Install Dependencies
1. Go to **Bash console** in PythonAnywhere
2. Run these commands:
```bash
cd /home/yourusername/level30app
source /home/yourusername/.virtualenvs/level30/bin/activate
pip install -r requirements.txt
```

### Step 5: Configure WSGI File
1. Go to **Web** tab
2. Find the **WSGI configuration file** line
3. Click on it (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
4. Replace the content with this:

```python
import sys
import os

project_dir = '/home/yourusername/level30app'
sys.path.insert(0, project_dir)

from app import app as application
```

### Step 6: Configure Static Files
1. In the **Web** tab, scroll to **Static files** section
2. Add these static file mappings:
   - **URL**: `/static/`  
     **Directory**: `/home/yourusername/level30app/static`
   
3. Add this for uploads:
   - **URL**: `/static/uploads/`  
     **Directory**: `/home/yourusername/level30app/static/uploads`

### Step 7: Reload Web App
1. Click the **Reload** button (green button at top of Web page)
2. Wait for the app to reload (should take a few seconds)
3. Your app will be at: `https://yourusername.pythonanywhere.com`

### Step 8: Test the Application
1. Open your app URL in a browser
2. Test all features:
   - Navigation between pages
   - Game voting
   - Scoreboard
   - Gewinnspiel (contest) upload and voting
   - Mobile responsiveness

## 🔧 Important Notes

### File Size Limits
- Free accounts: 100 MB total storage
- Uploads are limited by PythonAnywhere free tier
- If images don't upload, check free account limits

### Data Persistence
⚠️ **Important**: The current app uses **in-memory data storage**
- All votes, scores, and uploaded images are **lost when the app restarts**
- To keep data persistent, you need to upgrade to **paid PythonAnywhere** or add a database

### Recommended Upgrades for Persistence:
1. **Option A**: Upgrade to PythonAnywhere paid account (access to MySQL)
2. **Option B**: Use file-based storage (JSON files)
3. **Option C**: Use SQLite database

### For Production (Optional Database Setup)
If you want persistent storage, modify `app.py` to use SQLite:

```python
import sqlite3
from pathlib import Path

DB_FILE = Path('party_data.db')

def init_db():
    if not DB_FILE.exists():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # Create tables here
        conn.commit()
        conn.close()

init_db()
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Make sure you installed dependencies in the virtualenv

### Issue: Static files (CSS, images) not loading
**Solution**: Check that Static files mappings are correct in Web tab

### Issue: Uploads folder not writable
**Solution**: 
1. Go to Bash console
2. Run: `chmod -R 777 /home/yourusername/level30app/static/uploads`

### Issue: App returns 502 error
**Solution**:
1. Check error log in Web tab
2. Make sure WSGI file is correct
3. Try reloading the web app

### Issue: Images not appearing in Gewinnspiel
**Solution**: 
1. Verify uploads directory exists: `/static/uploads/`
2. Check file permissions
3. Upload file size must be < 5 MB

## 📱 Mobile Access

Once deployed, guests can access from any device on the internet:
- Desktop: `https://yourusername.pythonanywhere.com`
- Mobile: `https://yourusername.pythonanywhere.com` (fully responsive)

## 🔐 Security Notes

⚠️ **For Production Use**:
1. Change the `app.secret_key` to a random string
2. Set `debug=False` (already done)
3. Use HTTPS (PythonAnywhere provides this)
4. Consider adding authentication for moderator functions

## 📝 File Structure

Your PythonAnywhere project should look like:
```
/home/yourusername/level30app/
├── app.py
├── wsgi.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── spieluebersicht.html
│   ├── spiel.html
│   ├── scoreboard.html
│   ├── gewinnspiel.html
│   └── 404.html
├── static/
│   ├── style.css
│   ├── david.png
│   ├── spiel1.png
│   ├── spiel2.png
│   ├── spiel3.png
│   ├── spiel4.png
│   ├── spiel5.png
│   ├── spiel6.png
│   └── uploads/ (created automatically)
```

## ✅ Verification Checklist

After deployment, verify:
- [ ] Home page loads
- [ ] Navigation works (all menu items clickable)
- [ ] Games page displays all 6 games
- [ ] Voting system works
- [ ] Scoreboard updates correctly
- [ ] Gewinnspiel upload works
- [ ] Images display after upload
- [ ] Voting on images works
- [ ] Mobile menu (hamburger) works on small screens
- [ ] Responsive design looks good on all screen sizes

## 🎉 Success!

Your app should now be live on PythonAnywhere!

---

**Need Help?**
- PythonAnywhere Help: https://help.pythonanywhere.com
- Flask Documentation: https://flask.palletsprojects.com
- Contact: Check PythonAnywhere support forum

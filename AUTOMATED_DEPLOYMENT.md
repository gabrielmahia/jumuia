# Automatic Deployment Guide — Zero Manual Steps

**Goal:** Deploy to Streamlit Cloud with ONE command. No form-filling. Full automation.

---

## 🎯 **OPTION 1: ONE-COMMAND DEPLOYMENT** (Recommended)

### Prerequisites
- GitHub account (free)
- Streamlit Cloud account (free)
- Git installed locally

### Step 1: Fork Repository (Manual, one-time)

```bash
# Visit GitHub
https://github.com/gabrielmahia/catholic-network-tools
# Click "Fork"
# Select your account
# Done ✓
```

### Step 2: Run Auto-Deploy Script (Fully Automated)

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/catholic-network-tools.git
cd catholic-network-tools

# Make script executable
chmod +x deploy.sh

# Run deployment verification
./deploy.sh
```

**What the script does:**
- ✅ Verifies you're on `main` branch
- ✅ Confirms `app/01_Home.py` exists
- ✅ Checks `requirements.txt` is present
- ✅ Verifies `.streamlit/config.toml` exists
- ✅ Pushes commits to GitHub
- ✅ Shows deployment instructions

### Step 3: Connect to Streamlit Cloud (One-time Setup)

1. Visit https://streamlit.io/cloud
2. Click "Create new app"
3. Connect your GitHub account (authorize once)
4. In the form:
   - **Repository:** `YOUR-USERNAME/catholic-network-tools`
   - **Branch:** `main`
   - **Main file path:** `app/01_Home.py`
5. Click "Deploy"

**Takes 30-60 seconds. App is live!**

---

## 🚀 **OPTION 2: FULL AUTOMATION VIA GITHUB ACTIONS** (No Manual Deploy Needed)

Once you connect Streamlit Cloud to your GitHub repo, **every push automatically deploys**.

### How It Works

```
You push to GitHub
    ↓
GitHub Actions runs tests
    ↓
All tests pass
    ↓
Streamlit Cloud auto-detects changes
    ↓
App redeploys in 1-2 minutes
    ↓
Done! (You don't do anything)
```

### Setup (One Time)

1. Fork the repository (see Option 1, Step 1)
2. In Streamlit Cloud, connect GitHub account
3. Deploy the app (see Option 1, Step 3)
4. **From now on:** Every `git push` automatically redeploys

---

## 📝 **OPTION 3: COMMAND-LINE DEPLOYMENT**

If you want to test locally before deploying:

### Install Streamlit Locally

```bash
pip install -r requirements.txt
```

### Run App Locally

```bash
streamlit run app/01_Home.py
```

App opens at: `http://localhost:8501`

### Deploy to Cloud

```bash
streamlit run app/01_Home.py --logger.level=debug
# Then visit share.streamlit.io/deploy when prompted
```

---

## 🔧 **OPTION 4: PYTHON AUTOMATION SCRIPT**

For organizations wanting fully programmatic deployment:

```python
#!/usr/bin/env python3
"""Automated Streamlit deployment"""

import subprocess
import os
import sys

def deploy():
    # Configuration
    GITHUB_REPO = "gabrielmahia/catholic-network-tools"
    BRANCH = "main"
    MAIN_FILE = "app/01_Home.py"
    
    print("🚀 Streamlit Auto-Deploy")
    print("=" * 50)
    
    # 1. Verify git
    if not os.path.exists(".git"):
        print("❌ Not a git repository")
        sys.exit(1)
    
    # 2. Verify branch
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], 
                          capture_output=True, text=True)
    current_branch = result.stdout.strip()
    
    if current_branch != BRANCH:
        print(f"⚠️  Not on {BRANCH} branch (on {current_branch})")
        subprocess.run(["git", "checkout", BRANCH])
    
    # 3. Verify files
    required_files = [
        MAIN_FILE,
        "requirements.txt",
        ".streamlit/config.toml",
        "app/pages/02_Sacraments.py",
        "app/pages/03_Pastoral_Care.py",
        "app/pages/04_Justice.py",
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing: {file}")
            sys.exit(1)
    
    print(f"✓ All required files present")
    
    # 4. Push to GitHub
    print("\n📤 Pushing to GitHub...")
    subprocess.run(["git", "push", "origin", BRANCH])
    print("✓ Pushed")
    
    # 5. Instructions
    print("\n" + "=" * 50)
    print("✅ READY TO DEPLOY")
    print("=" * 50)
    print(f"""
Your app is ready for deployment!

To deploy to Streamlit Cloud:
1. Visit: https://share.streamlit.io/deploy
2. Select repository: {GITHUB_REPO}
3. Branch: {BRANCH}
4. Main file: {MAIN_FILE}
5. Click Deploy

OR use GitHub's direct integration:
1. Go to: https://streamlit.io/cloud
2. Connect your GitHub account
3. Select this repo
4. Click Deploy

Your app will be at:
https://gabrielmahia-catholic-network-tools.streamlit.app
    """)

if __name__ == "__main__":
    deploy()
```

Save as `scripts/deploy.py` and run:
```bash
python scripts/deploy.py
```

---

## 🎯 **QUICK REFERENCE**

### Fastest Way (You are here! 👇)

```bash
# 1. Fork on GitHub (1 minute)
https://github.com/gabrielmahia/catholic-network-tools → Fork

# 2. Connect to Streamlit Cloud (1 minute)
https://streamlit.io/cloud → Create new app → Select your fork

# 3. Fill form (1 minute)
Repository: YOUR-USERNAME/catholic-network-tools
Branch: main
Main file: app/01_Home.py

# 4. Click Deploy (30 seconds, automatic)

# DONE! Your app is live
```

### After First Deployment (Going Forward)

```bash
# Every time you update code:
git push origin main

# Streamlit Cloud auto-deploys in 1-2 minutes
# NO manual deployment needed
```

---

## 🔄 **AUTOMATED WORKFLOW**

Once setup, your workflow becomes:

```
1. Make code changes locally
2. git add . && git commit -m "message"
3. git push origin main
4. GitHub Actions runs tests
5. Streamlit Cloud auto-deploys (no action needed)
6. Your live app updates in 1-2 minutes
7. Done ✓
```

**Zero manual deployments after first setup.**

---

## ⚠️ **COMMON ISSUES & FIXES**

### "Branch does not exist"
**Fix:** Change branch from `master` to `main`

### "Main file does not exist"
**Fix:** Change from `streamlit_app.py` to `app/01_Home.py`

### "Deployment stuck"
**Fix:** Click "Reboot app" in Streamlit Cloud dashboard

### "Changes not showing"
**Fix:** Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

### "App crashes on deploy"
**Fix:** Check Streamlit Cloud logs (click app name → Logs tab)

---

## 📊 **DEPLOYMENT CHECKLIST**

- [ ] Repository forked on GitHub
- [ ] Pushed to GitHub (all commits)
- [ ] `app/01_Home.py` exists
- [ ] `requirements.txt` exists
- [ ] `.streamlit/config.toml` exists
- [ ] Connected Streamlit Cloud to GitHub
- [ ] Created app in Streamlit Cloud
- [ ] Filled deployment form correctly:
  - [ ] Repository: `YOUR-USERNAME/catholic-network-tools`
  - [ ] Branch: `main`
  - [ ] Main file: `app/01_Home.py`
- [ ] Clicked "Deploy"
- [ ] Waited 30-60 seconds for deployment
- [ ] App is live! ✓

---

## 🎁 **BONUS: KEEP APP UPDATED AUTOMATICALLY**

Your app auto-updates whenever you push to GitHub.

Example workflow:

```bash
# Local development
streamlit run app/01_Home.py  # Test locally

# Changes look good
git add .
git commit -m "feat: add new justice campaign"
git push origin main

# Streamlit Cloud auto-detects and deploys
# Your live app updates in ~1-2 minutes
# Parishioners see changes immediately
```

---

## 🚀 **YOU'RE AUTOMATED NOW**

After initial setup, deployment is **fully automated**.

Just push to GitHub. Streamlit handles the rest.

**Welcome to modern deployment.** 🎉

---

**Questions?**
- GitHub Issues: https://github.com/gabrielmahia/catholic-network-tools/issues
- Streamlit Docs: https://docs.streamlit.io
- Email: contact@aikungfu.dev

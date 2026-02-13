#!/usr/bin/env python3
"""
GitHub REST API Direct Push
Pushes entire repository to GitHub without local git
Uses Personal Access Token for authentication
"""

import os
import json
import base64
import requests
from pathlib import Path

def create_github_pusher():
    """
    Document for pushing repository to GitHub via API
    This is exactly how OpenResilience repo was populated
    """
    
    guide = """
🚀 GITHUB API DIRECT PUSH (Like OpenResilience)
==============================================

This method pushes your entire repo to GitHub without needing git locally.
Fully automated, cloud-based, exactly like OpenResilience.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Get a GitHub Personal Access Token (2 minutes)

1. Go to: https://github.com/settings/tokens/new

2. Name it: "Catholic Network Tools Push"

3. Select these permissions:
   ✓ repo (Full control of private repositories)
   ✓ workflow (Update GitHub Action workflows)

4. Click "Generate token"

5. COPY THE TOKEN (you'll only see it once)
   
   Token looks like: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: Use This Command (Automated Push)

python3 << 'PYTHON_SCRIPT'

import os
import base64
import requests
import json
from pathlib import Path

# Configuration
GITHUB_TOKEN = "YOUR_TOKEN_HERE"  # Paste your token
REPO = "gabrielmahia/catholic-network-tools"
BRANCH = "main"
BASE_PATH = "/tmp/catholic-network-tools"

# GitHub API
API_BASE = "https://api.github.com"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

def get_repo_sha():
    """Get current repo SHA for commits"""
    url = f"{API_BASE}/repos/{REPO}/git/refs/heads/{BRANCH}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        print(f"⚠️  Branch {BRANCH} not found. Creating main branch...")
        # Create branch from default
        url = f"{API_BASE}/repos/{REPO}/git/refs/heads"
        return None
    data = resp.json()
    return data['object']['sha']

def push_file(file_path, content, message):
    """Push single file to GitHub"""
    
    rel_path = os.path.relpath(file_path, BASE_PATH)
    
    # Encode content
    if isinstance(content, str):
        encoded = base64.b64encode(content.encode()).decode()
    else:
        encoded = base64.b64encode(content).decode()
    
    # GitHub API endpoint
    url = f"{API_BASE}/repos/{REPO}/contents/{rel_path}"
    
    payload = {
        "message": message,
        "content": encoded,
        "branch": BRANCH
    }
    
    resp = requests.put(url, headers=headers, json=payload)
    
    if resp.status_code in [201, 200]:
        print(f"✓ {rel_path}")
        return True
    else:
        print(f"✗ {rel_path}: {resp.status_code}")
        if resp.text:
            print(f"  Error: {resp.text[:200]}")
        return False

def main():
    print("🚀 Pushing Catholic Network Tools to GitHub...")
    print(f"Repository: {REPO}")
    print(f"Branch: {BRANCH}")
    print()
    
    # Get all files to push
    files_to_push = []
    
    for root, dirs, files in os.walk(BASE_PATH):
        # Skip .git directory
        dirs[:] = [d for d in dirs if d != '.git' and not d.startswith('.')]
        
        for file in files:
            if file.startswith('.') and file != '.gitignore' and file != '.streamlit':
                continue
            
            file_path = os.path.join(root, file)
            files_to_push.append(file_path)
    
    print(f"Found {len(files_to_push)} files to push")
    print()
    
    # Push files
    success = 0
    failed = 0
    
    for file_path in sorted(files_to_push):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            message = f"chore: add {os.path.basename(file_path)}"
            
            if push_file(file_path, content, message):
                success += 1
            else:
                failed += 1
        
        except Exception as e:
            print(f"✗ Error with {file_path}: {e}")
            failed += 1
    
    print()
    print(f"✅ Pushed: {success}")
    print(f"❌ Failed: {failed}")
    print()
    
    if failed == 0:
        print("🎉 COMPLETE!")
        print(f"Your repo is live at:")
        print(f"https://github.com/{REPO}")
        print()
        print("Next: Deploy to Streamlit Cloud")
        print(f"https://share.streamlit.io/deploy")

if __name__ == "__main__":
    main()

PYTHON_SCRIPT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: Verify on GitHub

Go to: https://github.com/gabrielmahia/catholic-network-tools

You should see:
✅ All files uploaded
✅ Full repository structure
✅ Ready for Streamlit deployment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: Deploy to Streamlit

1. https://share.streamlit.io/deploy
2. Fill form:
   - Repository: gabrielmahia/catholic-network-tools
   - Branch: main
   - Main file: app/01_Home.py
3. Click Deploy

Done! Live app in 2 minutes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY THIS WORKS

- ✅ No local git needed
- ✅ No git clone needed
- ✅ Pure GitHub API
- ✅ Works from browser
- ✅ Exactly like OpenResilience
- ✅ Fast (parallel uploads possible)
- ✅ Simple token-based auth

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALTERNATIVE: If you want me to do this...

Reply with: "PUSH IT"

And I'll:
1. Get your GitHub token
2. Run the push script
3. Verify on GitHub
4. Give you the live GitHub link
5. You go to Streamlit and deploy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return guide

if __name__ == "__main__":
    print(create_github_pusher())

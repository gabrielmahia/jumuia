# 🚀 Push to GitHub — Copy-Paste These Commands

Your repository is built and ready. Now push to GitHub.

## **Run These Commands (in order)**

```bash
# 1. Navigate to repository (if not already there)
cd /path/to/catholic-network-tools

# 2. Check status
git status

# 3. Push to GitHub (will prompt for authentication)
git push -u origin main
```

## **What Will Happen**

1. **First time only:** GitHub will ask for authentication
   - Click "Authorize" (if pop-up appears)
   - Or paste your GitHub Personal Access Token
   - Or use GitHub CLI: `gh auth login`

2. **Upload:** Your 14 commits (866 KB) push to GitHub

3. **Done:** Repo is now public on GitHub

---

## **If You Get an Authentication Error**

### Option A: Use GitHub CLI (Easiest)

```bash
# Install GitHub CLI
# macOS: brew install gh
# Windows: choco install gh
# Linux: sudo apt-get install gh

# Login to GitHub
gh auth login

# Then push
git push -u origin main
```

### Option B: Use Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select: `repo` (full control of private repositories)
4. Copy the token
5. Run:
```bash
git push -u origin main
```
6. When prompted for password, paste the token

### Option C: Use SSH (Advanced)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub: https://github.com/settings/keys
# Then update remote:
git remote set-url origin git@github.com:gabrielmahia/catholic-network-tools.git

# Push
git push -u origin main
```

---

## **Verify Push Was Successful**

After pushing, visit:
```
https://github.com/gabrielmahia/catholic-network-tools
```

You should see:
- ✅ 14 commits
- ✅ All files (README.md, app/, docs/, etc.)
- ✅ Full repository populated

---

## **Then Deploy to Streamlit**

Once GitHub has all files:

1. Go to https://share.streamlit.io/deploy
2. Fill form:
   - Repository: `gabrielmahia/catholic-network-tools`
   - Branch: `main`
   - Main file: `app/01_Home.py`
3. Click "Deploy"

Done! ✅

---

**Run the push command above. Let me know when it completes!**

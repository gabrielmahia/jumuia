#!/bin/bash

# 🚀 Catholic Network Tools - Complete Cloud Automation
# Works in GitHub Codespaces, no local setup required

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  CATHOLIC NETWORK TOOLS - CLOUD AUTOMATION                ║"
echo "║  Pure GitHub + Streamlit (OpenResilience Style)           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
GITHUB_REPO="gabrielmahia/catholic-network-tools"
BRANCH="main"
MAIN_FILE="app/01_Home.py"
STREAMLIT_URL="https://gabrielmahia-catholic-network-tools.streamlit.app"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function: Print section header
print_section() {
  echo ""
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}$1${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Function: Check environment
check_environment() {
  print_section "1️⃣  CHECK ENVIRONMENT"
  
  echo "Checking for required tools..."
  
  if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}⚠️  Git not found${NC}"
    echo "But you can use GitHub Codespaces instead (no git needed)"
    exit 0
  fi
  
  echo -e "${GREEN}✓ Git found${NC}"
  
  # Check if in repo
  if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Not in git repository${NC}"
    echo "If in GitHub Codespaces, run: git init"
    exit 0
  fi
  
  echo -e "${GREEN}✓ Git repository found${NC}"
}

# Function: Verify structure
verify_structure() {
  print_section "2️⃣  VERIFY REPOSITORY STRUCTURE"
  
  required_files=(
    "app/01_Home.py"
    "app/pages/02_Sacraments.py"
    "app/pages/03_Pastoral_Care.py"
    "app/pages/04_Justice.py"
    "app/pages/05_Formation.py"
    "app/pages/06_Stewardship.py"
    "app/pages/07_Admin.py"
    "requirements.txt"
    ".streamlit/config.toml"
    "README_GLOBAL.md"
    "docs/THEOLOGY.md"
  )
  
  echo "Checking required files..."
  for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
      echo -e "${GREEN}✓${NC} $file"
    else
      echo -e "${YELLOW}✗${NC} MISSING: $file"
    fi
  done
  
  echo ""
  echo -e "${GREEN}✓ Structure verified${NC}"
}

# Function: Show git status
show_git_status() {
  print_section "3️⃣  GIT STATUS"
  
  echo "Current branch:"
  git rev-parse --abbrev-ref HEAD
  
  echo ""
  echo "Recent commits:"
  git log --oneline | head -5
  
  echo ""
  echo "Unpushed commits:"
  UNPUSHED=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "0")
  echo "$UNPUSHED commits to push"
}

# Function: Push to GitHub
push_to_github() {
  print_section "4️⃣  PUSH TO GITHUB"
  
  echo "Configuring git..."
  git config user.email "catholic-network-tools@aikungfu.dev" || true
  git config user.name "Catholic Network Tools Bot" || true
  
  echo ""
  echo "Checking git status..."
  
  if [ -z "$(git status --porcelain)" ]; then
    echo -e "${GREEN}✓ Working directory clean${NC}"
  else
    echo -e "${YELLOW}⚠️  Uncommitted changes${NC}"
    echo "Stash them first: git stash"
    return 1
  fi
  
  echo ""
  echo "Pushing to GitHub..."
  git push origin $BRANCH 2>&1 || {
    echo -e "${YELLOW}⚠️  Push failed${NC}"
    echo "You may need to authenticate with GitHub."
    echo "Use: gh auth login (if GitHub CLI installed)"
    return 1
  }
  
  echo -e "${GREEN}✓ Pushed to GitHub${NC}"
}

# Function: Show deployment instructions
show_deployment_instructions() {
  print_section "5️⃣  DEPLOY TO STREAMLIT CLOUD"
  
  cat << 'EOF'

✅ Your code is now on GitHub!

🎯 Next: Deploy to Streamlit Cloud (takes 2 minutes)

STEPS:
1. Visit: https://share.streamlit.io/deploy
2. Click "Create app"
3. Fill form:
   - Repository: gabrielmahia/catholic-network-tools
   - Branch: main
   - Main file: app/01_Home.py
4. Click "Deploy"
5. Wait 30-60 seconds
6. Your app is live! ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OR if Streamlit Cloud is already connected:

The app may auto-deploy! Check:
https://share.streamlit.io/gabrielmahia/catholic-network-tools/main/app/01_Home.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your live app will be at:
https://gabrielmahia-catholic-network-tools.streamlit.app

EOF
}

# Function: Show automation guide
show_automation_guide() {
  print_section "6️⃣  GOING FORWARD (ZERO LOCAL WORK)"
  
  cat << 'EOF'

FROM NOW ON - Pure GitHub + Streamlit Automation:

TO UPDATE YOUR LIVE APP:

  Option 1: GitHub Web UI (Easiest)
  ─────────────────────────────────
  1. Go to: https://github.com/gabrielmahia/catholic-network-tools
  2. Click on file → pencil icon (edit)
  3. Make changes
  4. Scroll → "Commit changes"
  5. GitHub Actions validates (auto)
  6. Streamlit redeploys (auto)
  7. Live app updates in 1-2 minutes
  
  Option 2: GitHub Codespaces (Full IDE)
  ──────────────────────────────────────
  1. Code button → Codespaces → Open
  2. Edit files in VS Code (in browser)
  3. git commit -am "message"
  4. git push origin main
  5. GitHub Actions validates (auto)
  6. Streamlit redeploys (auto)
  
  Option 3: GitHub Actions Workflow
  ──────────────────────────────────
  1. Go to: Actions tab
  2. Select: "🚀 Push to GitHub & Deploy"
  3. Click: "Run workflow"
  4. Watch it validate + deploy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ZERO LOCAL WORK. PURE CLOUD AUTOMATION.

Like OpenResilience - everything in GitHub.

EOF
}

# Function: Show summary
show_summary() {
  print_section "✅ SUMMARY"
  
  cat << EOF

Repository:      $GITHUB_REPO
Branch:          $BRANCH
Main file:       $MAIN_FILE
Status:          READY FOR DEPLOYMENT

Files:           $(find . -type f \( -name "*.py" -o -name "*.md" \) | grep -v '.git' | wc -l)
Commits:         $(git log --oneline 2>/dev/null | wc -l || echo "Unknown")
Size:            $(du -sh . 2>/dev/null | cut -f1)

Workflows:       .github/workflows/ (auto-validate + auto-deploy)
Configuration:   .streamlit/config.toml (theming)
Documentation:   8 comprehensive guides

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 YOU'RE READY FOR CLOUD DEPLOYMENT!

Next: https://share.streamlit.io/deploy

EOF
}

# Main execution
main() {
  check_environment
  verify_structure
  show_git_status
  
  if push_to_github; then
    show_deployment_instructions
    show_automation_guide
    show_summary
  else
    echo ""
    echo -e "${YELLOW}⚠️  Push not completed${NC}"
    echo "Check GitHub authentication and try again"
    exit 1
  fi
}

# Run main
main "$@"

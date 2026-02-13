#!/bin/bash
# Streamlit automatic deployment script
# Usage: ./deploy.sh

set -e

echo "🚀 Catholic Network Tools — Automated Streamlit Deployment"
echo "==========================================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if streamlit CLI is installed
if ! command -v streamlit &> /dev/null; then
    echo -e "${YELLOW}Installing Streamlit CLI...${NC}"
    pip install streamlit --quiet
fi

# Configuration
REPO_URL="https://github.com/gabrielmahia/catholic-network-tools"
BRANCH="main"
MAIN_FILE="app/01_Home.py"
APP_NAME="catholic-network-tools"

echo -e "${GREEN}✓ Configuration:${NC}"
echo "  Repository: $REPO_URL"
echo "  Branch: $BRANCH"
echo "  Main file: $MAIN_FILE"
echo "  App name: $APP_NAME"
echo ""

# Step 1: Verify repository
echo -e "${YELLOW}Step 1: Verifying repository...${NC}"
if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git repository found${NC}"
    git remote -v
else
    echo -e "${RED}✗ Not a git repository${NC}"
    exit 1
fi

# Step 2: Check branch
echo ""
echo -e "${YELLOW}Step 2: Checking branch...${NC}"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" == "$BRANCH" ]; then
    echo -e "${GREEN}✓ On correct branch: $BRANCH${NC}"
else
    echo -e "${YELLOW}⚠ Not on $BRANCH (currently on $CURRENT_BRANCH)${NC}"
    echo "Checking out $BRANCH..."
    git checkout $BRANCH
fi

# Step 3: Verify main file exists
echo ""
echo -e "${YELLOW}Step 3: Verifying main file...${NC}"
if [ -f "$MAIN_FILE" ]; then
    echo -e "${GREEN}✓ Main file exists: $MAIN_FILE${NC}"
else
    echo -e "${RED}✗ Main file not found: $MAIN_FILE${NC}"
    exit 1
fi

# Step 4: Check requirements.txt
echo ""
echo -e "${YELLOW}Step 4: Checking dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✓ requirements.txt found${NC}"
    echo "  Dependencies:"
    cat requirements.txt | sed 's/^/    /'
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    exit 1
fi

# Step 5: Ensure .streamlit config exists
echo ""
echo -e "${YELLOW}Step 5: Checking Streamlit config...${NC}"
if [ -f ".streamlit/config.toml" ]; then
    echo -e "${GREEN}✓ Streamlit config found${NC}"
else
    echo -e "${RED}✗ Streamlit config missing${NC}"
    exit 1
fi

# Step 6: Push to GitHub (if there are unpushed commits)
echo ""
echo -e "${YELLOW}Step 6: Syncing with GitHub...${NC}"
if [ -n "$(git status --porcelain)" ]; then
    echo "Uncommitted changes found. Stash them first:"
    echo "  git stash"
    exit 1
else
    echo -e "${GREEN}✓ Working directory clean${NC}"
fi

# Check if there are commits to push
UNPUSHED=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "0")
if [ "$UNPUSHED" -gt 0 ]; then
    echo "Pushing $UNPUSHED commits to GitHub..."
    git push origin $BRANCH
    echo -e "${GREEN}✓ Pushed to GitHub${NC}"
else
    echo -e "${GREEN}✓ Already up to date with GitHub${NC}"
fi

# Step 7: Display deployment info
echo ""
echo "==========================================================="
echo -e "${GREEN}✓ READY TO DEPLOY${NC}"
echo "==========================================================="
echo ""
echo "To deploy to Streamlit Cloud:"
echo ""
echo "1. Go to: https://share.streamlit.io/deploy"
echo "2. Fill in:"
echo "   - Repository: gabrielmahia/catholic-network-tools"
echo "   - Branch: main"
echo "   - Main file path: app/01_Home.py"
echo "3. Click Deploy"
echo ""
echo "OR use Streamlit CLI:"
echo "   streamlit run app/01_Home.py"
echo ""
echo "Your app will be live at:"
echo "   https://gabrielmahia-catholic-network-tools.streamlit.app"
echo ""

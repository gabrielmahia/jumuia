#!/bin/bash
# push_to_github.sh
# ─────────────────────────────────────────────────────────────
# Catholic Network Tools — GitHub Push Script
# Run this ONCE after creating your GitHub repository.
#
# USAGE:
#   chmod +x push_to_github.sh
#   ./push_to_github.sh https://github.com/YOUR_USERNAME/catholic-network-tools.git
#
# PREREQUISITES:
#   - Create an empty repo at github.com (no README, no .gitignore)
#   - Have a Personal Access Token (PAT) ready
#     Get one at: https://github.com/settings/tokens/new
#     Scopes needed: repo (full)
# ─────────────────────────────────────────────────────────────

set -e

REMOTE_URL="${1}"

if [ -z "$REMOTE_URL" ]; then
  echo "❌  Usage: ./push_to_github.sh https://github.com/YOUR_USERNAME/your-repo.git"
  exit 1
fi

echo "🔗  Setting remote: $REMOTE_URL"
git remote add origin "$REMOTE_URL"

echo "⬆️   Pushing 7 commits to main..."
git push -u origin main

echo ""
echo "✅  Done. Your repository is live."
echo ""
echo "Next step — open a PR if working from a feature branch, or"
echo "go to your repo and verify the Actions tab shows CI passing."
echo ""
echo "Streamlit Cloud deployment:"
echo "  1. Visit: https://share.streamlit.io"
echo "  2. New app → connect this repo → main branch → app.py"
echo "  3. Add secrets: ANTHROPIC_API_KEY (and optionally M-Pesa + AT keys)"

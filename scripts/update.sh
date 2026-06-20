#!/usr/bin/env bash
# Update client from GitHub — discards local code edits, keeps .env
# Usage: bash scripts/update.sh
# Then:  sudo systemctl restart <client>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BRANCH="${DEPLOY_GIT_BRANCH:-main}"

echo "==> fetch origin/${BRANCH}"
git fetch origin "${BRANCH}"

echo "==> reset code to origin/${BRANCH} (keeps .env — not in git)"
git reset --hard "origin/${BRANCH}"

bash "$(dirname "$0")/deploy.sh"

echo ""
echo "==> update complete — restart gunicorn:"
echo "    sudo systemctl restart ahmedatef   # or sweb, etc."

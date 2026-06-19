#!/usr/bin/env bash
# Automated deploy steps for LyomasTech salon instances.
# Usage (on server): bash scripts/deploy.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -f .venv/bin/activate ]]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

echo "==> migrate"
python manage.py migrate --noinput

echo "==> ensure deploy superuser"
python manage.py ensure_deploy_superuser

echo "==> collectstatic"
python manage.py collectstatic --noinput

echo "==> deploy complete"
echo "    Login: LyomasTech@\${DEPLOY_CLIENT_NAME:-<subdomain>} / check DEPLOY_SUPERUSER_PASSWORD in .env"

#!/usr/bin/env bash
# Generate per-client deploy files from templates.
#
# Usage:
#   bash deploy/new-client.sh sweb Sweb
#   bash deploy/new-client.sh sweb Sweb 'MyDbPassword123'
#
# Output: deploy/generated/<client>/
set -euo pipefail

CLIENT_SLUG="${1:?Client slug required, e.g. sweb}"
CLIENT_NAME="${2:?Client display name required, e.g. Sweb}"
DB_PASSWORD="${3:-CHANGE_ME_db_password}"
DOMAIN="${CLIENT_SLUG}.erpbylyomastech.com"
DB_NAME="${CLIENT_SLUG}db"
DB_USER="${CLIENT_SLUG}_user"
SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))' 2>/dev/null || openssl rand -base64 48)"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/deploy/generated/${CLIENT_SLUG}"
mkdir -p "$OUT"

render() {
  local src="$1"
  local dest="$2"
  sed \
    -e "s|{{CLIENT_SLUG}}|${CLIENT_SLUG}|g" \
    -e "s|{{CLIENT_NAME}}|${CLIENT_NAME}|g" \
    -e "s|{{DOMAIN}}|${DOMAIN}|g" \
    -e "s|{{DB_NAME}}|${DB_NAME}|g" \
    -e "s|{{DB_USER}}|${DB_USER}|g" \
    -e "s|{{DB_PASSWORD}}|${DB_PASSWORD}|g" \
    -e "s|{{GENERATE_UNIQUE_SECRET_KEY}}|${SECRET_KEY}|g" \
    "$src" > "$dest"
}

render "$ROOT/deploy/templates/env.client.template" "$OUT/.env"
render "$ROOT/deploy/templates/nginx-http.conf.template" "$OUT/nginx.conf"
render "$ROOT/deploy/templates/gunicorn.service.template" "$OUT/gunicorn.service"

cat > "$OUT/README.txt" <<EOF
Generated for client: ${CLIENT_SLUG}
Domain: https://${DOMAIN}
Superuser: LyomasTech@${CLIENT_NAME}
Password: Lyo@22999 (or DEPLOY_SUPERUSER_PASSWORD in .env)

Copy files:
  .env            -> /var/www/${CLIENT_SLUG}/.env
  nginx.conf      -> /etc/nginx/sites-available/${CLIENT_SLUG}
  gunicorn.service -> /etc/systemd/system/${CLIENT_SLUG}.service

PostgreSQL:
  CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
  CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
EOF

echo "Generated: $OUT"
ls -la "$OUT"

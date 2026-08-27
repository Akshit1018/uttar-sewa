#!/usr/bin/env bash
# Serve the PWA + API on :8000 and publish a Cloudflare quick tunnel.
# The trycloudflare.com URL is ephemeral. Control writes stay loopback-only
# unless CONTROL_TOKEN is set. Do not treat this as a production deploy.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PORT="${PORT:-8000}"
CLOUDFLARED_BIN="${CLOUDFLARED_BIN:-cloudflared}"

if ! command -v "$CLOUDFLARED_BIN" >/dev/null 2>&1; then
  if [ -x /tmp/cloudflared ]; then
    CLOUDFLARED_BIN=/tmp/cloudflared
  else
    echo "cloudflared not found. Install: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
    exit 1
  fi
fi

if [ ! -f frontend/build/index.html ]; then
  echo "Building PWA (omit REACT_APP_BACKEND_URL so the page origin is the API)..."
  (cd frontend && yarn install --frozen-lockfile && yarn build)
fi

if ! curl -sf "http://127.0.0.1:${PORT}/api/health" >/dev/null 2>&1; then
  echo "Starting API on :${PORT}..."
  python3 -m uvicorn backend.server:app --host 127.0.0.1 --port "${PORT}" &
  UVICORN_PID=$!
  trap 'kill ${UVICORN_PID} 2>/dev/null || true' EXIT
  for _ in $(seq 1 40); do
    if curl -sf "http://127.0.0.1:${PORT}/api/health" >/dev/null 2>&1; then
      break
    fi
    sleep 0.5
  done
fi

echo "Opening Cloudflare quick tunnel to http://127.0.0.1:${PORT}"
exec "$CLOUDFLARED_BIN" tunnel --no-autoupdate --url "http://127.0.0.1:${PORT}"

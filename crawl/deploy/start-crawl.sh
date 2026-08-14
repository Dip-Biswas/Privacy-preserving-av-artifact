#!/usr/bin/env bash
# One-shot: setup env (if needed), launch crawl workers + monitor.
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"
COUNTRY_CODE="${COUNTRY_CODE:?set COUNTRY_CODE}"
GCS_BUCKET="${GCS_BUCKET:?set GCS_BUCKET}"

cd "$HOME/crawler"
if [ ! -d .venv ] && [ ! -f uv.lock ]; then
  echo "ERROR: crawler not installed at $HOME/crawler"
  exit 1
fi
if ! command -v uv >/dev/null 2>&1; then
  bash "$HOME/deploy/setup.sh"
fi
if ! uv run python -c "import selenium" >/dev/null 2>&1; then
  bash "$HOME/deploy/setup.sh"
fi

pkill -f 'python main.py' 2>/dev/null || true
pkill -f 'deploy/monitor.sh' 2>/dev/null || true
sleep 1

export COUNTRY_CODE GCS_BUCKET
nohup bash "$HOME/deploy/launch.sh" > "$HOME/launch.log" 2>&1 &
sleep 8
nohup bash "$HOME/deploy/monitor.sh" > "$HOME/monitor.log" 2>&1 &
sleep 5

echo "PAGES=$(find "$HOME/pages" -maxdepth 1 -name '*.html' 2>/dev/null | wc -l)"
echo "WORKERS=$(pgrep -fc 'main.py' || echo 0)"
tail -n 3 "$HOME/launch.log"
tail -n 2 "$HOME/logs/worker-0.log" 2>/dev/null || true

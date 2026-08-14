#!/usr/bin/env bash
# Installs everything the crawler needs on a fresh Ubuntu VM.
# Idempotent: safe to re-run.
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

echo "==> apt packages"
sudo apt-get update -y
sudo apt-get install -y \
  wget curl gnupg ca-certificates \
  xvfb tmux xxd python3 python3-venv

echo "==> Google Chrome"
if ! command -v google-chrome >/dev/null 2>&1; then
  wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
  rm -f google-chrome-stable_current_amd64.deb
fi
google-chrome --version

echo "==> uv"
if ! command -v uv >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/uv" ]; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"
uv --version

echo "==> python env (uv sync)"
cd "$HOME/crawler"
uv sync

echo "==> setup complete"

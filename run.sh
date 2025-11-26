#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
else
  echo "[ERROR] Python 3 is not installed or not on PATH." >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "[INFO] Creating virtual environment (.venv)..."
  "$PYTHON_CMD" -m venv .venv
fi

source .venv/bin/activate

echo "[INFO] Installing/updating dependencies from requirements.txt..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt >/dev/null

PORT="${1:-8501}"

echo "[INFO] Starting Streamlit on http://localhost:${PORT}"
streamlit run app.py --server.port "$PORT" --server.address "127.0.0.1"

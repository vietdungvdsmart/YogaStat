#!/bin/bash
set -e

# Change to this script's directory
cd "$(dirname "$0")"

# Choose Python interpreter (prefer python3, fallback to python)
PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python 3 is not installed or not on PATH."
    echo "        Install from https://www.python.org/downloads/ and try again."
    exit 1
fi

# Create venv if missing
if [ ! -d ".venv" ]; then
    echo "[INFO] Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment."
        exit 1
    fi
fi

# Activate venv
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment."
    exit 1
fi

# Upgrade pip and install dependencies
python -m pip install --upgrade pip >/dev/null
echo "[INFO] Installing dependencies..."
python -m pip install --upgrade streamlit plotly pandas numpy requests >/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install Python packages."
    exit 1
fi

# Allow optional port argument, default 5000
PORT=${1:-5000}

# Start Streamlit
echo "[INFO] Starting Streamlit..."
echo "[INFO] Access the app at: http://localhost:$PORT"
echo "[INFO] Press Ctrl+C to stop the server"
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT

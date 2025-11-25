## YogaStat - Local Run Guide

### Prerequisites
- Python 3.11+ installed and on PATH
- Internet access to install packages

### Quick start (recommended)
1. Run the script from project root:
```bash
./run.sh
```
   Optional custom port:
```bash
./run.sh 8502
```
2. Open your browser: `http://localhost:5000` (or your chosen port).

### Manual setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 5000
```

### Access from another device (same network)
- Allow inbound on the chosen port (firewall).
- Use your machine's LAN IP: `http://YOUR_LAN_IP:5000`.

### Troubleshooting
- "This site can't be reached": ensure Streamlit is running and the port is open.
- If port is busy, pass another port to `./run.sh`.
- Check logs in the terminal where Streamlit started.

### Data input
- Enter your n8n webhook URL in the app sidebar and click "Fetch Data".
- Or load sample data from the home screen to explore the dashboard.


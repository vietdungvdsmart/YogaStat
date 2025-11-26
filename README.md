## YogaStat – Local Run Guide

This repo no longer depends on Replit tooling. Everything is wired for a standard local Streamlit workflow.

### Requirements
- Python 3.11+
- `pip` and a POSIX-compatible shell (macOS/Linux/WSL). On Windows PowerShell, swap `source` for `.venv\\Scripts\\activate`.

### Quick start
```bash
./run.sh          # creates .venv if needed, installs deps, launches Streamlit on 127.0.0.1:8501
./run.sh 8502     # same, but custom port
```
The script is idempotent—it always installs from `requirements.txt`.

### Manual setup (equivalent steps)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
streamlit run app.py
```

### Configuration & secrets
- Theme/default Streamlit settings live in `.streamlit/config.toml`. Update or remove to suit your environment.
- Put any private keys in `.streamlit/secrets.toml` (already gitignored) and read them via `st.secrets`.

### Data input
- Provide your n8n webhook URL in the app sidebar to fetch live analytics.
- Or load the bundled sample data from the home screen for a quick demo.

### Troubleshooting
- Port already in use → pass a different port to `run.sh`/`streamlit run`.
- App can’t reach your webhook → verify the URL and your network connection.
- UI not updating after edits → restart `streamlit run app.py` or set `server.runOnSave = true` in `.streamlit/config.toml`.

### Webhook data format
- The webhook should return an array of country blocks. Each block looks like:
  ```json
  [
    {
      "country": "VN",
      "data": [
        {
          "time": 20250301,
          "first_open": 4,
          "...": "...",
          "notification_receive": 120,
          "notification_open": 48,
          "notification_dismiss": 30,
          "click_banner": 10,
          "click_notification": 9
        }
      ]
    },
    { "country": "India", "data": [ ... ] },
    { "country": "US", "data": [ ... ] }
  ]
  ```
- The dashboard merges all countries into an “All Countries” tab automatically and still lets you inspect each country individually.
- New notification/broadcast metrics (`notification_receive`, `notification_open`, `notification_dismiss`, `click_banner`, `click_notification`) are required if you want the notification insights and charts to light up. All metrics are counted in **users**; `avg_engage_time` remains in seconds.

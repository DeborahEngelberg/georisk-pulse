# GeoRisk Pulse

Geopolitical risk monitoring dashboard that scrapes news headlines from Reuters, AP, and Al Jazeera, scores them using NLP, and visualizes 30-day risk trends.

## Features

- **RSS Scraping** — Pulls headlines from Reuters, AP, and Al Jazeera RSS feeds
- **NLP Scoring** — Uses spaCy + keyword-weighted model to assign daily risk scores (0–100) per region
- **SQLite Storage** — Stores headline metadata and daily scores
- **Plotly Dashboard** — Interactive line chart showing 30-day risk trends
- **Email Digest** — Daily summary of top 3 risk movers via SendGrid
- **Auto-scheduling** — Runs pipeline daily at 6:00 UTC via APScheduler

## Monitored Regions

Iran, Russia, Israel, Taiwan (configurable in `scraper.py`)

## Quick Start

```bash
# Clone and enter the project
cd georisk_pulse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Run the app
python app.py
```

Open http://localhost:5000. Click **"Run Pipeline Now"** to fetch initial data.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `PORT` | No | Server port (default: 5000) |
| `SENDGRID_API_KEY` | No | SendGrid API key for email digest |
| `DIGEST_FROM_EMAIL` | No | Sender email for digest |
| `DIGEST_TO_EMAIL` | No | Recipient email for digest |
| `GEORISK_DB` | No | SQLite database path (default: `georisk.db`) |
| `GEORISK_CHART_DAYS` | No | Days to show in chart (default: 30) |

Email digest is optional — the app works without SendGrid configured.

## Deploy on Railway / Render

### Railway

1. Push to GitHub
2. Connect repo in Railway dashboard
3. Railway auto-detects the `Procfile`
4. Add environment variables in the Settings tab
5. Add a build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`

### Render

1. Push to GitHub
2. Create a new **Web Service** in Render
3. Set **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. Set **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add environment variables in the Environment tab

> **Note:** Free-tier instances on Railway/Render spin down after inactivity. The scheduler runs within the web process, so the daily pipeline only fires while the instance is awake. For reliable daily runs, use an external cron service (e.g., cron-job.org) to hit `POST /run` daily.

## Running the Pipeline Manually

```bash
# From the command line
python scheduler.py

# Or via HTTP
curl -X POST http://localhost:5000/run
```

## Project Structure

```
georisk_pulse/
├── app.py           # Flask web app + scheduler
├── scraper.py       # RSS feed fetching + region matching
├── scorer.py        # spaCy NLP scoring model
├── database.py      # SQLite operations
├── emailer.py       # SendGrid email digest
├── scheduler.py     # Pipeline orchestrator (also CLI entry point)
├── templates/
│   └── index.html   # Dashboard with Plotly chart
├── requirements.txt
├── Procfile         # For Railway/Render
└── runtime.txt      # Python version
```

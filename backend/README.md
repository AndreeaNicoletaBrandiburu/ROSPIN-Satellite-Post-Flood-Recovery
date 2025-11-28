# Backend API

Flask REST API for the Post-Flood Recovery Analysis platform.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

The API will start on `http://localhost:5000`

## Endpoints

- `GET /api/health` - Health check
- `POST /api/process-flood-event` - Process flood event
- `GET /api/recovery-metrics/<event_id>` - Get recovery metrics
- `GET /api/events` - List all events
- `GET /api/dashboard-data` - Dashboard data
- `POST /api/survival-analysis/predict` - Recovery prediction

## Environment Variables

Create a `.env` file with:
```
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
```


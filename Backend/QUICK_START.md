# Quick Start Guide

## Start the Backend Server

```bash
cd Backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Or use the startup script:
```bash
./start.sh
```

## Verify It's Working

1. **Health Check**: Open http://localhost:8000/health
2. **API Docs**: Open http://localhost:8000/docs

## Add Sample Data

```bash
python sample_client.py
```

## Frontend Connection

The backend is configured to accept requests from:
- http://localhost:5173 (Vite default)
- http://localhost:3000 (Alternative port)

Make sure your frontend is running on one of these ports, or update `CORS_ORIGINS` in `.env`.


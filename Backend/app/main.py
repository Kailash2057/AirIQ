'''
This is the entry point of the backend.

Loads .env file.

Creates database tables automatically.

Configures CORS (so frontend can call APIs).

Adds /health endpoint.

Includes all routers:

/api/v1/ingest

/api/v1/sensors

/api/v1/map

/api/v1/readings

Start the server with:

uvicorn app.main:app --reload
'''

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .db import Base, engine
from .models import Sensor, Reading
from .routes import ingest, sensors, map_latest, readings

load_dotenv()

API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",")]

# Create tables on startup (SQLite dev convenience)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AirIQ Sprint 3 Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(ingest.router, prefix=API_V1_PREFIX)
app.include_router(sensors.router, prefix=API_V1_PREFIX)
app.include_router(map_latest.router, prefix=API_V1_PREFIX)

app.include_router(readings.router, prefix=API_V1_PREFIX)

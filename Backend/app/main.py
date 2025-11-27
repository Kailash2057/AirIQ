'''
This is the entry point of the backend.

Loads .env file.

Initializes MongoDB connection.

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
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .db import init_db, close_db
from .routes import ingest, sensors, map_latest, readings

load_dotenv()

API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",")]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize MongoDB
    await init_db()
    yield
    # Shutdown: Close MongoDB connection
    await close_db()

app = FastAPI(
    title="AirIQ Backend",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "database": "mongodb"}

app.include_router(ingest.router, prefix=API_V1_PREFIX)
app.include_router(sensors.router, prefix=API_V1_PREFIX)
app.include_router(map_latest.router, prefix=API_V1_PREFIX)
app.include_router(readings.router, prefix=API_V1_PREFIX)

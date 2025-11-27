"""Purpose: receive sensor data from Raspberry Pi.

Flow:

Checks the API key in header:
Authorization: Bearer pi-key-1

Validates JSON body using IngestPayload.

Creates a new Sensor if it doesn't exist.

Inserts a new Reading record.

Returns { "ok": true, "sensor_id": "..." }"""

from fastapi import APIRouter, Depends, Header, HTTPException, status
from ..schemas import IngestPayload
from ..models import Reading, Sensor
from ..services.aqi import pm25_to_aqi
import os

router = APIRouter(prefix="/ingest", tags=["ingest"])

def require_device_key(authorization: str = Header(default="")):
    keys = {k.strip() for k in os.getenv("DEVICE_API_KEYS", "").split(",") if k.strip()}
    try:
        scheme, token = authorization.split(" ", 1)
    except ValueError:
        scheme, token = "", ""
    if scheme.lower() != "bearer" or token not in keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid device key")
    return True

@router.post("")
async def ingest(payload: IngestPayload, _: bool = Depends(require_device_key)):
    # Upsert sensor if missing
    sensor = await Sensor.get(payload.sensor_id)
    if not sensor:
        sensor = Sensor(
            id=payload.sensor_id,
            status="active"
        )
        await sensor.insert()
    
    # Calculate AQI from PM2.5 value
    aqi_value, aqi_category = pm25_to_aqi(payload.pm25)
    
    # Create reading with calculated AQI
    reading = Reading(
        sensor_id=payload.sensor_id,
        ts=payload.ts,
        pm25=payload.pm25,
        pm10=payload.pm10,
        co2=payload.co2,
        no2=payload.no2,
        temp_c=payload.temp_c,
        rh=payload.rh,
        battery=payload.battery,
        firmware=payload.firmware,
        raw_json=payload.model_dump(),
    )
    await reading.insert()
    
    return {
        "ok": True,
        "sensor_id": payload.sensor_id,
        "aqi": aqi_value,
        "aqi_category": aqi_category,
        "timestamp": payload.ts.isoformat() if hasattr(payload.ts, 'isoformat') else str(payload.ts)
    }

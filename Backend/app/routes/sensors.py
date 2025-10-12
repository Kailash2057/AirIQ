'''
Provides operations about sensors.

GET /api/v1/sensors

Returns a list of all sensors (id, status, coordinates, etc.).

GET /api/v1/sensors/{sensor_id}/latest

Returns the most recent reading for one sensor, plus AQI info.

PATCH /api/v1/sensors/{sensor_id}

Allows you to update metadata (name, lat/lon, label, status).
'''


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from ..models import Sensor, Reading
from ..schemas import SensorOut, ReadingOut
from ..services.aqi import pm25_to_aqi
from pydantic import BaseModel

from fastapi import Body, HTTPException, status

class SensorUpdate(BaseModel):
    name: str | None = None
    model: str | None = None
    lat: float | None = None
    lon: float | None = None
    location_label: str | None = None
    status: str | None = None

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.get("", response_model=list[SensorOut])
def list_sensors(db: Session = Depends(get_db)):
    return db.scalars(select(Sensor)).all()

@router.get("/{sensor_id}/latest", response_model=ReadingOut | None)
def latest(sensor_id: str, db: Session = Depends(get_db)):
    stmt = (
        select(Reading)
        .where(Reading.sensor_id == sensor_id)
        .order_by(Reading.ts.desc())
        .limit(1)
    )
    row = db.scalars(stmt).first()
    if not row:
        return None
    aqi, cat = pm25_to_aqi(row.pm25)
    return ReadingOut(
        sensor_id=row.sensor_id,
        ts=row.ts,
        pm25=row.pm25,
        pm10=row.pm10,
        co2=row.co2,
        no2=row.no2,
        temp_c=row.temp_c,
        rh=row.rh,
        battery=row.battery,
        firmware=row.firmware,
        aqi_pm25=aqi,
        aqi_category=cat
    )

@router.patch("/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: str, payload: SensorUpdate = Body(...), db: Session = Depends(get_db)):
    s = db.get(Sensor, sensor_id)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    if payload.name is not None: s.name = payload.name
    if payload.model is not None: s.model = payload.model
    if payload.lat is not None: s.lat = payload.lat
    if payload.lon is not None: s.lon = payload.lon
    if payload.location_label is not None: s.location_label = payload.location_label
    if payload.status is not None: s.status = payload.status
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

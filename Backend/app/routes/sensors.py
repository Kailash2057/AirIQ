'''
Provides operations about sensors.

GET /api/v1/sensors

Returns a list of all sensors (id, status, coordinates, etc.).

GET /api/v1/sensors/{sensor_id}/latest

Returns the most recent reading for one sensor, plus AQI info.

PATCH /api/v1/sensors/{sensor_id}

Allows you to update metadata (name, lat/lon, label, status).
'''

from fastapi import APIRouter, Body, HTTPException, status
from ..models import Sensor, Reading
from ..schemas import SensorOut, ReadingOut
from ..services.aqi import pm25_to_aqi
from pydantic import BaseModel
from typing import Optional

class SensorUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    location_label: Optional[str] = None
    status: Optional[str] = None

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.get("", response_model=list[SensorOut])
async def list_sensors():
    sensors = await Sensor.find_all().to_list()
    return sensors

@router.get("/{sensor_id}/latest", response_model=ReadingOut | None)
async def latest(sensor_id: str):
    readings = await Reading.find(
        Reading.sensor_id == sensor_id
    ).sort("-ts").limit(1).to_list()
    
    if not readings:
        return None
    
    reading = readings[0]
    
    aqi, cat = pm25_to_aqi(reading.pm25)
    return ReadingOut(
        sensor_id=reading.sensor_id,
        ts=reading.ts,
        pm25=reading.pm25,
        pm10=reading.pm10,
        co2=reading.co2,
        no2=reading.no2,
        temp_c=reading.temp_c,
        rh=reading.rh,
        battery=reading.battery,
        firmware=reading.firmware,
        aqi_pm25=aqi,
        aqi_category=cat
    )

@router.patch("/{sensor_id}", response_model=SensorOut)
async def update_sensor(sensor_id: str, payload: SensorUpdate = Body(...)):
    sensor = await Sensor.get(sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sensor, key, value)
    
    await sensor.save()
    return sensor

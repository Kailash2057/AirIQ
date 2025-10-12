'''
Defines Pydantic models (how data looks coming in or going out):

IngestPayload → expected JSON from the Pi

SensorOut → what /sensors returns

ReadingOut → what reading endpoints return (includes AQI fields)

Pydantic validates types and converts strings → floats/datetimes automatically.
'''

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class IngestPayload(BaseModel):
    sensor_id: str = Field(..., example="RPI-ENG-HALL-01")
    ts: datetime
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    co2: Optional[float] = None
    no2: Optional[float] = None
    temp_c: Optional[float] = None
    rh: Optional[float] = None
    battery: Optional[float] = None
    firmware: Optional[str] = None

class SensorOut(BaseModel):
    id: str
    name: str | None = None
    lat: float | None = None
    lon: float | None = None
    location_label: str | None = None
    status: str

    class Config:
        orm_mode = True

class ReadingOut(BaseModel):
    sensor_id: str
    ts: datetime
    pm25: float | None = None
    pm10: float | None = None
    co2: float | None = None
    no2: float | None = None
    temp_c: float | None = None
    rh: float | None = None
    battery: float | None = None
    firmware: str | None = None
    aqi_pm25: int | None = None
    aqi_category: str | None = None

    class Config:
        orm_mode = True

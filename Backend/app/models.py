'''
Defines MongoDB document models using Beanie ODM:

Sensor
Field	      Description
id	         Unique sensor ID (e.g., "RPI-ENG-HALL-01")
name / model	Optional description
lat / lon	    Coordinates for map display
location_label	Human-friendly location name
installed_at	Auto-timestamp when added
status	Active, inactive, etc.

Reading
Field	     Description
id	         Auto-generated MongoDB ObjectId
sensor_id	Reference to Sensor.id
ts	       Timestamp of the reading
pm25, pm10, co2, no2, temp_c, rh	Measured values
battery	Battery percentage
firmware	Version string
raw_json	Original JSON payload

Every Sensor can have many Readings.
'''

from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional

class Sensor(Document):
    """Sensor document model"""
    id: str = Field(..., description="Unique sensor ID (e.g., 'RPI-ENG-HALL-01')")
    name: Optional[str] = None
    model: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    location_label: Optional[str] = None
    installed_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "active"

    class Settings:
        name = "sensors"  # Collection name
        indexes = [
            "id",  # Index on sensor ID
        ]

class Reading(Document):
    """Reading document model"""
    sensor_id: str = Field(..., description="Reference to Sensor.id")
    ts: datetime = Field(..., description="Timestamp of the reading")
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    co2: Optional[float] = None
    no2: Optional[float] = None
    temp_c: Optional[float] = None
    rh: Optional[float] = None
    battery: Optional[float] = None
    firmware: Optional[str] = None
    raw_json: Optional[dict] = None

    class Settings:
        name = "readings"  # Collection name
        indexes = [
            "sensor_id",  # Index on sensor_id for fast lookups
            "ts",  # Index on timestamp for time-based queries
            [("sensor_id", 1), ("ts", -1)],  # Compound index for sensor + time queries
        ]

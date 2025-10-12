'''
Defines database tables (ORM models):

Sensor
Field	      Description
id	         Unique sensor ID (e.g., “RPI-ENG-HALL-01”)
name / model	Optional description
lat / lon	    Coordinates for map display
location_label	Human-friendly location name
installed_at	Auto-timestamp when added
status	Active, inactive, etc.

Reading
Field	     Description
id	         Auto number
sensor_id	Foreign key → Sensor.id
ts	       Timestamp of the reading
pm25, pm10, co2, no2, temp_c, rh	Measured values
battery	Battery percentage
firmware	Version string
raw_json	Original JSON payload

Every Sensor can have many Readings.
'''


from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, text, Index
from sqlalchemy.orm import relationship
from .db import Base

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(String, primary_key=True)  # e.g., "RPI-ENG-HALL-01"
    name = Column(String, nullable=True)
    model = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    location_label = Column(String, nullable=True)
    installed_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(String, default="active")
    readings = relationship("Reading", back_populates="sensor", cascade="all,delete-orphan")

class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(String, ForeignKey("sensors.id"), index=True, nullable=False)
    ts = Column(DateTime, index=True, nullable=False)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    co2 = Column(Float, nullable=True)
    no2 = Column(Float, nullable=True)
    temp_c = Column(Float, nullable=True)
    rh = Column(Float, nullable=True)
    battery = Column(Float, nullable=True)
    firmware = Column(String, nullable=True)
    raw_json = Column(JSON, nullable=True)

    sensor = relationship("Sensor", back_populates="readings")

Index("idx_readings_sensor_ts", Reading.sensor_id, Reading.ts.desc())

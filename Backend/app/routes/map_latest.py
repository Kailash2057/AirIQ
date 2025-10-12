'''
Purpose: used by the map dashboard.

Returns one object per sensor:

{
  "sensor_id": "RPI-ENG-HALL-01",
  "ts": "2025-10-12T18:00:00Z",
  "pm25": 12.5,
  "aqi_pm25": 50,
  "aqi_category": "Good",
  "lat": 32.7313,
  "lon": -97.1106,
  "location_label": "Engineering Hall Lobby"
}


The frontend plots pins using lat/lon and colors them by AQI.
'''

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from ..db import get_db
from ..models import Reading, Sensor
from ..services.aqi import pm25_to_aqi

router = APIRouter(prefix="/map", tags=["map"])

@router.get("/latest")
def map_latest(db: Session = Depends(get_db)):
    # For each sensor, pick the max(ts) reading
    # SQLite approach: subquery to get latest ts per sensor
    subq = (
        select(Reading.sensor_id, func.max(Reading.ts).label("max_ts"))
        .group_by(Reading.sensor_id)
        .subquery()
    )
    join_stmt = (
        select(Reading, Sensor)
        .join(subq, (Reading.sensor_id == subq.c.sensor_id) & (Reading.ts == subq.c.max_ts))
        .join(Sensor, Sensor.id == Reading.sensor_id)
    )
    out = []
    for r, s in db.execute(join_stmt).all():
        aqi, cat = pm25_to_aqi(r.pm25)
        out.append({
            "sensor_id": r.sensor_id,
            "ts": r.ts.isoformat() if r.ts else None,
            "pm25": r.pm25, "pm10": r.pm10, "co2": r.co2, "no2": r.no2,
            "temp_c": r.temp_c, "rh": r.rh,
            "aqi_pm25": aqi, "aqi_category": cat,
            "lat": s.lat, "lon": s.lon, "location_label": s.location_label
        })
    return out

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

from fastapi import APIRouter
from ..models import Reading, Sensor
from ..services.aqi import pm25_to_aqi

router = APIRouter(prefix="/map", tags=["map"])

@router.get("/latest")
async def map_latest():
    # Get all sensors
    sensors = await Sensor.find_all().to_list()
    
    out = []
    for sensor in sensors:
        # Get latest reading for this sensor
        readings = await Reading.find(
            Reading.sensor_id == sensor.id
        ).sort("-ts").limit(1).to_list()
        
        if readings:
            reading = readings[0]
            aqi, cat = pm25_to_aqi(reading.pm25)
            # Handle datetime serialization
            ts_str = None
            if reading.ts:
                if isinstance(reading.ts, str):
                    ts_str = reading.ts
                else:
                    ts_str = reading.ts.isoformat()
            
            out.append({
                "sensor_id": reading.sensor_id,
                "ts": ts_str,
                "pm25": reading.pm25,
                "pm10": reading.pm10,
                "co2": reading.co2,
                "no2": reading.no2,
                "temp_c": reading.temp_c,
                "rh": reading.rh,
                "aqi_pm25": aqi,
                "aqi_category": cat,
                "lat": sensor.lat,
                "lon": sensor.lon,
                "location_label": sensor.location_label
            })
    
    return out

'''
A mini script that simulates a Raspberry Pi.
It:

Generates random sensor values

Sends them to POST /api/v1/ingest

Prints the server’s response
Use it to confirm the backend works before connecting real hardware.
'''

import os, json, time, random
import requests
from datetime import datetime, timezone

API = os.getenv("API", "http://localhost:8000/api/v1/ingest")
DEVICE_KEY = os.getenv("DEVICE_KEY", "pi-key-1")
SENSOR_ID = os.getenv("SENSOR_ID", "RPI-ENG-HALL-01")

def mock():
    return {
        "pm25": round(random.uniform(5, 35), 1),
        "pm10": round(random.uniform(10, 60), 1),
        "co2": round(random.uniform(500, 1200), 0),
        "no2": round(random.uniform(0.005, 0.03), 3),
        "temp_c": round(random.uniform(20, 28), 1),
        "rh": round(random.uniform(30, 60), 1),
        "battery": 100.0,
        "firmware": "1.0.0",
    }

if __name__ == "__main__":
    payload = {"sensor_id": SENSOR_ID, "ts": datetime.now(timezone.utc).isoformat(), **mock()}
    r = requests.post(API, headers={"Authorization": f"Bearer {DEVICE_KEY}"}, json=payload, timeout=5)
    print(r.status_code, r.text)

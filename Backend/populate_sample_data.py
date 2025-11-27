#!/usr/bin/env python3
"""
Populate MongoDB with sample sensor data for testing.
Creates multiple sensors with readings over the past 30 days.
"""

import asyncio
import random
from datetime import datetime, timedelta, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

from app.models import Sensor, Reading

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGODB_DATABASE", "airiq")

# Single sensor location
SENSOR = {
    "id": "AIRIQ-SENSOR-01",
    "name": "Air Quality Monitoring Station",
    "lat": 32.7313,  # Update with your actual location
    "lon": -97.1106,  # Update with your actual location
    "location_label": "Main Monitoring Location"  # Update with your location name
}

def generate_reading(base_time, sensor_id, variation=0):
    """Generate a realistic sensor reading"""
    # Base values with some variation
    hour = base_time.hour
    
    # Simulate daily patterns
    temp_base = 22 + 3 * math.sin((hour - 6) * math.pi / 12)  # Warmer during day
    humidity_base = 50 + 10 * math.cos((hour - 6) * math.pi / 12)  # Higher at night
    co2_base = 600 + 200 * (1 + math.sin((hour - 8) * math.pi / 12))  # Higher during occupied hours
    
    return {
        "sensor_id": sensor_id,
        "ts": base_time,
        "pm25": round(random.uniform(5 + variation, 35 + variation), 1),
        "pm10": round(random.uniform(10 + variation, 60 + variation), 1),
        "co2": round(random.uniform(co2_base - 100, co2_base + 200), 0),
        "no2": round(random.uniform(0.005, 0.03), 3),
        "temp_c": round(temp_base + random.uniform(-2, 2) + variation * 0.5, 1),
        "rh": round(humidity_base + random.uniform(-5, 5) + variation, 1),
        "battery": round(random.uniform(85, 100), 1),
        "firmware": "1.0.0"
    }

async def populate_data():
    """Populate database with sample data"""
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGODB_URL)
    await init_beanie(
        database=client[DATABASE_NAME],
        document_models=[Sensor, Reading]
    )
    
    print("Creating sensor...")
    # Create or update sensor
    existing = await Sensor.get(SENSOR["id"])
    if existing:
        print(f"  Sensor {SENSOR['id']} already exists, updating...")
        for key, value in SENSOR.items():
            setattr(existing, key, value)
        await existing.save()
    else:
        sensor = Sensor(**SENSOR, status="active")
        await sensor.insert()
        print(f"  Created sensor: {SENSOR['id']}")
    
    print("\nGenerating readings...")
    now = datetime.now(timezone.utc)
    
    # Generate readings for the past 30 days
    # Create readings every 2 hours for the past 30 days
    total_readings = 0
    for days_ago in range(30):
        date = now - timedelta(days=days_ago)
        for hour in range(0, 24, 2):  # Every 2 hours
            reading_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            # Generate reading for the single sensor
            reading_data = {
                "sensor_id": SENSOR["id"],
                    "ts": reading_time,
                    "pm25": round(random.uniform(5, 35), 1),
                    "pm10": round(random.uniform(10, 60), 1),
                    "co2": round(random.uniform(500, 1200), 0),
                    "no2": round(random.uniform(0.005, 0.03), 3),
                    "temp_c": round(20 + random.uniform(-3, 5), 1),
                    "rh": round(40 + random.uniform(-10, 20), 1),
                    "battery": round(random.uniform(85, 100), 1),
                    "firmware": "1.0.0"
                }
                
                reading = Reading(**reading_data)
                await reading.insert()
                total_readings += 1
    
    print(f"\n✓ Successfully created {total_readings} readings for sensor {SENSOR['id']}")
    print(f"✓ Data spans the last 30 days")
    print(f"\nYou can now view the data at:")
    print(f"  Frontend: http://localhost:3000")
    print(f"  API: http://localhost:8003/api/v1/sensors")
    
    client.close()

if __name__ == "__main__":
    import math
    asyncio.run(populate_data())


#!/usr/bin/env python3
"""
Test script to simulate Raspberry Pi sending data to backend
and verify the complete data flow.
"""

import requests
import json
from datetime import datetime, timezone, timedelta
import time

BACKEND_URL = "http://localhost:8003"
API_ENDPOINT = f"{BACKEND_URL}/api/v1/ingest"
DEVICE_KEY = "pi-key-1"

def send_sensor_reading(sensor_id, pm25, co2, temp, humidity, hours_ago=0):
    """Send a sensor reading to the backend"""
    reading_time = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    
    payload = {
        "sensor_id": sensor_id,
        "ts": reading_time.isoformat(),
        "pm25": pm25,
        "pm10": pm25 * 1.5,  # Estimate PM10 from PM2.5
        "co2": co2,
        "no2": 0.015,
        "temp_c": temp,
        "rh": humidity,
        "battery": 95.0,
        "firmware": "1.0.0"
    }
    
    headers = {
        "Authorization": f"Bearer {DEVICE_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Sent reading for {sensor_id}: AQI={result.get('aqi')} ({result.get('aqi_category')})")
            return True
        else:
            print(f"✗ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error sending data: {e}")
        return False

def test_complete_flow():
    """Test the complete data flow"""
    SENSOR_ID = "AIRIQ-SENSOR-01"  # Single sensor
    
    print("=" * 60)
    print("Testing Complete AirIQ Data Flow (Single Sensor)")
    print("=" * 60)
    print()
    
    # Test 1: Send current reading
    print("1. Sending current sensor reading...")
    send_sensor_reading(SENSOR_ID, 15.5, 750, 24.1, 48.0, hours_ago=0)
    time.sleep(1)
    
    # Test 2: Send readings for today (for daily chart)
    print("\n2. Sending readings for today (hourly data)...")
    for hour in range(24):
        pm25 = 10 + (hour % 12) * 2  # Vary PM2.5 throughout day
        co2 = 600 + (hour % 8) * 50
        temp = 20 + (hour % 12) * 0.5
        humidity = 40 + (hour % 10) * 2
        
        send_sensor_reading(SENSOR_ID, pm25, co2, temp, humidity, hours_ago=23-hour)
        time.sleep(0.1)
    
    # Test 3: Send readings for past 30 days (for monthly chart)
    print("\n3. Sending readings for past 30 days (daily data)...")
    for day in range(30):
        pm25 = 12 + (day % 7) * 3
        co2 = 650 + (day % 10) * 30
        temp = 22 + (day % 5) * 1
        humidity = 45 + (day % 8) * 2
        
        # Send one reading per day
        send_sensor_reading(SENSOR_ID, pm25, co2, temp, humidity, hours_ago=day*24)
        time.sleep(0.1)
    
    print("\n" + "=" * 60)
    print("✓ Complete flow test finished!")
    print("=" * 60)
    print("\nVerify data at:")
    print(f"  - Frontend: http://localhost:3000")
    print(f"  - Backend API: {BACKEND_URL}/docs")
    print(f"  - Sensors: {BACKEND_URL}/api/v1/sensors")
    print(f"  - Latest: {BACKEND_URL}/api/v1/map/latest")

if __name__ == "__main__":
    test_complete_flow()


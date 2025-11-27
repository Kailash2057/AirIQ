#!/usr/bin/env python3
"""
Quick test script to verify backend is working.
Tests all main endpoints.
"""

import requests
import json
from datetime import datetime, timezone, timedelta

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"
DEVICE_KEY = "pi-key-1"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print(f"✓ Health check passed: {response.json()}\n")

def test_ingest():
    """Test data ingestion"""
    print("Testing /ingest endpoint...")
    payload = {
        "sensor_id": "RPI-TEST-01",
        "ts": datetime.now(timezone.utc).isoformat(),
        "pm25": 15.5,
        "pm10": 25.0,
        "co2": 750,
        "no2": 0.015,
        "temp_c": 24.5,
        "rh": 50.0,
        "battery": 95,
        "firmware": "1.0.0"
    }
    headers = {"Authorization": f"Bearer {DEVICE_KEY}"}
    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/ingest",
        headers=headers,
        json=payload
    )
    assert response.status_code == 200
    print(f"✓ Ingest test passed: {response.json()}\n")

def test_sensors():
    """Test sensors endpoint"""
    print("Testing /sensors endpoint...")
    response = requests.get(f"{BASE_URL}{API_PREFIX}/sensors")
    assert response.status_code == 200
    sensors = response.json()
    print(f"✓ Sensors endpoint passed: Found {len(sensors)} sensor(s)\n")
    return sensors

def test_map_latest():
    """Test map/latest endpoint"""
    print("Testing /map/latest endpoint...")
    response = requests.get(f"{BASE_URL}{API_PREFIX}/map/latest")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Map latest endpoint passed: Found {len(data)} reading(s)\n")
    return data

def test_readings():
    """Test readings endpoint"""
    print("Testing /readings endpoint...")
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=1)).isoformat()
    end = now.isoformat()
    
    response = requests.get(
        f"{BASE_URL}{API_PREFIX}/readings",
        params={"start": start, "end": end, "limit": 100}
    )
    assert response.status_code == 200
    readings = response.json()
    print(f"✓ Readings endpoint passed: Found {len(readings)} reading(s)\n")
    return readings

if __name__ == "__main__":
    print("=" * 50)
    print("AirIQ Backend Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_ingest()
        test_sensors()
        test_map_latest()
        test_readings()
        
        print("=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to backend.")
        print("  Make sure the server is running on http://localhost:8000")
        print("  Start it with: uvicorn app.main:app --reload --port 8000")
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


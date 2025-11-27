# Single Sensor Setup Guide

## Overview

This guide is for setting up **one sensor** at **one location** for the AirIQ system.

## Quick Setup

### 1. Configure Sensor ID

**On Raspberry Pi**, set the sensor ID:

```bash
export AIRIQ_SENSOR_ID="AIRIQ-SENSOR-01"
```

Or edit `raspberry_pi_client.py`:
```python
SENSOR_ID = "AIRIQ-SENSOR-01"
```

### 2. Configure Backend URL

**On Raspberry Pi**, set your backend server URL:

```bash
export AIRIQ_BACKEND_URL="http://your-backend-ip:8003"
```

Replace `your-backend-ip` with your actual backend server IP address.

### 3. Configure API Key

**On Raspberry Pi**, set the device API key (must match backend .env):

```bash
export AIRIQ_DEVICE_KEY="pi-key-1"
```

**On Backend**, ensure `.env` has:
```env
DEVICE_API_KEYS=pi-key-1
```

### 4. Update Sensor Location (Optional)

If you want to set the sensor's location coordinates, you can update it via API:

```bash
curl -X PATCH "http://localhost:8003/api/v1/sensors/AIRIQ-SENSOR-01" \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 32.7313,
    "lon": -97.1106,
    "location_label": "Your Location Name"
  }'
```

Or it will be auto-created when the first reading is sent.

## Data Flow (Single Sensor)

```
Raspberry Pi (1 sensor)
    ↓
raspberry_pi_client.py
    ↓
Backend API (/api/v1/ingest)
    ↓
MongoDB (stores readings)
    ↓
Frontend (displays data)
```

## Testing

### Test Sensor Connection

```bash
# On Raspberry Pi
python3 raspberry_pi_client.py
```

### Verify Data Reception

```bash
# On Backend Server
curl http://localhost:8003/api/v1/sensors
curl http://localhost:8003/api/v1/map/latest
```

### View in Frontend

Open http://localhost:3000 to see the data displayed.

## Configuration Summary

**Raspberry Pi Environment Variables:**
```bash
AIRIQ_BACKEND_URL=http://your-backend-ip:8003
AIRIQ_DEVICE_KEY=pi-key-1
AIRIQ_SENSOR_ID=AIRIQ-SENSOR-01
AIRIQ_INTERVAL=300  # 5 minutes
```

**Backend .env:**
```env
DEVICE_API_KEYS=pi-key-1
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=airiq
```

That's it! The system is now configured for a single sensor location.


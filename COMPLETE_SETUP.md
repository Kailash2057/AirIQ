# AirIQ Complete Setup Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Raspberry Pi (Sensor Node)                │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  PM2.5   │  │   CO2    │  │   NO2    │  │  DHT22    │  │
│  │  Sensor  │  │  Sensor  │  │  Sensor  │  │  Temp/Hum │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │             │             │             │          │
│       └─────────────┴─────────────┴─────────────┘          │
│                          │                                   │
│                   raspberry_pi_client.py                    │
│                          │                                   │
│                    HTTP POST /api/v1/ingest                 │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend Server                          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           FastAPI Application                       │    │
│  │                                                      │    │
│  │  1. Receive sensor data                             │    │
│  │  2. Validate payload                                │    │
│  │  3. Calculate AQI from PM2.5                        │    │
│  │  4. Store in MongoDB                                 │    │
│  └──────────────────┬─────────────────────────────────┘    │
│                     │                                        │
│                     ▼                                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │              MongoDB Database                       │    │
│  │                                                      │    │
│  │  Collections:                                       │    │
│  │  - sensors (metadata)                               │    │
│  │  - readings (time-series data)                      │    │
│  └──────────────────┬─────────────────────────────────┘    │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      │ HTTP GET /api/v1/*
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  App.tsx                                            │    │
│  │                                                      │    │
│  │  1. Fetch latest data                               │    │
│  │  2. Fetch historical data                           │    │
│  │  3. Transform for charts                            │    │
│  │  4. Display metrics & visualizations                │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Backend Setup (Already Done)

```bash
cd Backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8003
```

### 2. Frontend Setup (Already Done)

```bash
cd Frontend
npm install
npm run dev
```

### 3. Raspberry Pi Setup

**On Raspberry Pi:**

```bash
# Install dependencies
pip install requests RPi.GPIO adafruit-circuitpython-dht pyserial

# Configure client
export AIRIQ_BACKEND_URL="http://your-backend-ip:8003"
export AIRIQ_DEVICE_KEY="pi-key-1"
export AIRIQ_SENSOR_ID="RPI-LOCATION-01"

# Run client
python3 raspberry_pi_client.py
```

## Data Flow Details

### Step 1: Sensor Data Collection (Raspberry Pi)

**File**: `raspberry_pi_client.py`

- Reads sensors every 5 minutes (configurable)
- Collects: PM2.5, PM10, CO2, NO2, Temperature, Humidity
- Creates JSON payload with UTC timestamp
- Sends via HTTP POST with Bearer token authentication

### Step 2: Backend Processing

**File**: `app/routes/ingest.py`

1. **Authentication**: Validates `Authorization: Bearer <key>` header
2. **Validation**: Uses Pydantic to validate payload structure
3. **Sensor Management**: Auto-creates sensor if new
4. **AQI Calculation**: Calculates Air Quality Index from PM2.5
5. **Storage**: Saves to MongoDB with timestamp
6. **Response**: Returns success with calculated AQI

### Step 3: Data Storage (MongoDB)

**Collections**:
- `sensors`: Sensor metadata (id, name, location, status)
- `readings`: Time-series sensor data with AQI

**Indexes**:
- `sensor_id` for fast lookups
- `ts` for time-based queries
- Compound index on `(sensor_id, ts)` for efficient queries

### Step 4: Frontend Display

**Files**:
- `src/utils/api.ts`: API communication
- `src/utils/dataTransform.ts`: Data transformation
- `src/App.tsx`: Main dashboard

**Process**:
1. Fetches latest reading from `/api/v1/map/latest`
2. Fetches historical data from `/api/v1/readings`
3. Transforms data for chart components
4. Displays real-time metrics and historical charts

## Testing the Complete Flow

### Test with Simulated Data

```bash
# On backend server
cd Backend
python3 test_complete_flow.py
```

This will:
- Send current reading
- Send 24 hourly readings (for daily chart)
- Send 30 daily readings (for monthly chart)

### Verify Data Flow

1. **Check Backend Logs**:
   ```bash
   tail -f /tmp/airiq_backend.log
   ```

2. **Check MongoDB**:
   ```bash
   mongosh airiq
   db.readings.countDocuments()
   db.readings.find().sort({ts: -1}).limit(1).pretty()
   ```

3. **Check Frontend**:
   - Open http://localhost:3000
   - Verify data appears in charts
   - Check metrics show current values

## Configuration

### Backend (.env)
```env
API_V1_PREFIX=/api/v1
DEVICE_API_KEYS=pi-key-1,pi-key-2,pi-key-3
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=airiq
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Raspberry Pi Client
```bash
export AIRIQ_BACKEND_URL="http://your-backend-ip:8003"
export AIRIQ_DEVICE_KEY="pi-key-1"
export AIRIQ_SENSOR_ID="RPI-LOCATION-01"
export AIRIQ_INTERVAL="300"  # 5 minutes
```

### Frontend
The frontend automatically connects to `http://localhost:8003` by default.
To change, set `VITE_API_BASE_URL` environment variable.

## API Endpoints

### Ingest (Raspberry Pi → Backend)
```
POST /api/v1/ingest
Headers: Authorization: Bearer <device-key>
Body: {
  "sensor_id": "RPI-ENG-HALL-01",
  "ts": "2025-11-27T22:00:00Z",
  "pm25": 15.5,
  "pm10": 25.0,
  "co2": 750,
  "no2": 0.012,
  "temp_c": 24.1,
  "rh": 48.0,
  "battery": 95,
  "firmware": "1.0.0"
}
```

### Frontend → Backend
```
GET /api/v1/map/latest          # Latest reading per sensor
GET /api/v1/readings            # Historical readings
GET /api/v1/sensors             # List all sensors
```

## Troubleshooting

### Raspberry Pi Can't Connect
- Check network connectivity
- Verify BACKEND_URL is correct
- Check firewall rules
- Verify API key matches backend .env

### Backend Not Receiving Data
- Check backend logs: `tail -f /tmp/airiq_backend.log`
- Verify MongoDB is running
- Check API key authentication

### Frontend Not Showing Data
- Check browser console for errors
- Verify backend is running on correct port
- Check CORS settings in backend .env
- Verify API endpoints return data

## Production Deployment

1. **Use HTTPS** for all API calls
2. **Set up monitoring** and alerts
3. **Implement rate limiting** on backend
4. **Use environment variables** for all secrets
5. **Set up automated backups** for MongoDB
6. **Configure logging** and log rotation
7. **Use process managers** (systemd, PM2) for services


# AirIQ Backend Setup Guide

## Quick Start

### 1. Create Virtual Environment (if not already created)
```bash
python3 -m venv .venv
```

### 2. Activate Virtual Environment
```bash
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the Backend directory with:
```env
API_V1_PREFIX=/api/v1
DEVICE_API_KEYS=pi-key-1,pi-key-2,pi-key-3
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=airiq
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:5174
```

### 4a. Start MongoDB
Make sure MongoDB is running. See `MONGODB_SETUP.md` for installation instructions.

### 5. Start the Server
```bash
# Option 1: Using the startup script
./start.sh

# Option 2: Direct command
uvicorn app.main:app --reload --port 8000
```

The server will start on `http://localhost:8000`

## API Endpoints

- **Health Check**: `GET /health`
- **API Documentation**: `GET /docs` (Swagger UI)
- **Alternative Docs**: `GET /redoc` (ReDoc)

### Main Endpoints:
- `POST /api/v1/ingest` - Receive sensor data (requires Bearer token)
- `GET /api/v1/sensors` - List all sensors
- `GET /api/v1/sensors/{sensor_id}/latest` - Get latest reading for a sensor
- `PATCH /api/v1/sensors/{sensor_id}` - Update sensor metadata
- `GET /api/v1/map/latest` - Get latest reading per sensor (for map view)
- `GET /api/v1/readings` - Get historical readings (with query params: sensor_id, start, end, limit)

## Testing the Backend

### Test with sample data:
```bash
# Post a sample reading
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Authorization: Bearer pi-key-1" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "RPI-ENG-HALL-01",
    "ts": "2025-01-15T18:00:00Z",
    "pm25": 12.5,
    "pm10": 20.0,
    "co2": 750,
    "no2": 0.012,
    "temp_c": 24.1,
    "rh": 48.0,
    "battery": 95,
    "firmware": "1.0.0"
  }'

# Get all sensors
curl "http://localhost:8000/api/v1/sensors"

# Get latest readings for map
curl "http://localhost:8000/api/v1/map/latest"

# Get readings for today
curl "http://localhost:8000/api/v1/readings?start=2025-01-15T00:00:00Z&end=2025-01-15T23:59:59Z"
```

## Database

The backend uses MongoDB. Make sure MongoDB is running before starting the server.

Collections:
- `sensors` - Sensor metadata (id, name, location, status)
- `readings` - Sensor readings (timestamped measurements)

## Troubleshooting

1. **Port already in use**: Change the port in the uvicorn command: `--port 8001`
2. **CORS errors**: Make sure your frontend URL is in `CORS_ORIGINS` in `.env`
3. **MongoDB connection errors**: Make sure MongoDB is running. Check `MONGODB_URL` in `.env`
4. **Import errors**: Make sure you're in the Backend directory and virtual environment is activated


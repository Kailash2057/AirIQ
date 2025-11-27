# AirIQ Data Flow Documentation

## Complete Data Pipeline

```
┌─────────────────┐
│  Raspberry Pi   │
│   (Sensors)     │
│                 │
│  - PM2.5/PM10   │
│  - CO2          │
│  - NO2          │
│  - Temp/Humid   │
└────────┬────────┘
         │
         │ HTTP POST
         │ /api/v1/ingest
         │
         ▼
┌─────────────────┐
│   Backend API   │
│   (FastAPI)     │
│                 │
│  1. Validate    │
│  2. Calculate   │
│     AQI         │
│  3. Store in    │
│     MongoDB     │
└────────┬────────┘
         │
         │ MongoDB
         │
         ▼
┌─────────────────┐
│    MongoDB      │
│                 │
│  Collections:  │
│  - sensors      │
│  - readings     │
└────────┬────────┘
         │
         │ HTTP GET
         │ /api/v1/*
         │
         ▼
┌─────────────────┐
│   Frontend      │
│   (React)       │
│                 │
│  - Fetch data   │
│  - Transform    │
│  - Display      │
│    charts       │
└─────────────────┘
```

## Step-by-Step Process

### 1. Raspberry Pi Data Collection

**File**: `raspberry_pi_client.py`

**Process**:
- Reads physical sensors every 5 minutes (configurable)
- Collects: PM2.5, PM10, CO2, NO2, Temperature, Humidity, Battery
- Creates JSON payload with timestamp
- Sends to backend via HTTP POST

**Example Payload**:
```json
{
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

### 2. Backend Processing

**File**: `app/routes/ingest.py`

**Process**:
1. **Authentication**: Validates API key from header
2. **Validation**: Validates payload structure using Pydantic
3. **Sensor Management**: Creates sensor record if doesn't exist
4. **AQI Calculation**: Calculates Air Quality Index from PM2.5
5. **Data Storage**: Stores reading in MongoDB
6. **Response**: Returns success with AQI values

**AQI Calculation** (`app/services/aqi.py`):
- PM2.5 → AQI mapping:
  - ≤ 12.0 → 50 (Good)
  - ≤ 35.4 → 100 (Moderate)
  - ≤ 55.4 → 150 (USG)
  - ≤ 150.4 → 200 (Unhealthy)
  - ≤ 250.4 → 300 (Very Unhealthy)
  - > 250.4 → 400 (Hazardous)

**MongoDB Storage**:
- **sensors** collection: Sensor metadata
- **readings** collection: All sensor readings with timestamps

### 3. Frontend Data Retrieval

**Files**: 
- `src/utils/api.ts` - API calls
- `src/utils/dataTransform.ts` - Data transformation
- `src/App.tsx` - Main component

**Process**:
1. **Fetch Current Data**: Gets latest reading from `/api/v1/map/latest`
2. **Fetch Historical Data**: Gets readings for charts from `/api/v1/readings`
3. **Transform Data**: Converts backend format to chart format
4. **Display**: Shows metrics, charts, and status indicators

**API Endpoints Used**:
- `GET /api/v1/map/latest` - Latest reading per sensor
- `GET /api/v1/readings` - Historical readings with filters
- `GET /api/v1/sensors` - Sensor list

## Data Transformations

### Backend → Frontend

**Current Reading**:
```javascript
// Backend format
{
  sensor_id: "RPI-ENG-HALL-01",
  ts: "2025-11-27T22:00:00Z",
  temp_c: 24.1,
  rh: 48.0,
  co2: 750
}

// Frontend format
{
  temperature: 24.1,
  humidity: 48.0,
  co2: 750,
  timestamp: Date
}
```

**Historical Data**:
- Backend: Array of readings with timestamps
- Frontend: Aggregated by hour (daily) or day (monthly)

## Real-Time Updates

### Automatic Refresh
- Frontend auto-refreshes every 30 minutes
- Manual refresh button available
- Backend processes new data immediately when received

### Data Flow Timing
1. **Raspberry Pi**: Sends data every 5 minutes
2. **Backend**: Processes and stores immediately
3. **Frontend**: Fetches latest data on load and refresh

## Error Handling

### Raspberry Pi Client
- Retry logic: 3 attempts with exponential backoff
- Logging: All errors logged to `/var/log/airiq-sensor.log`
- Graceful degradation: Continues even if some sensors fail

### Backend
- Validation errors: Returns 400 with error details
- Authentication errors: Returns 401
- Database errors: Logged and returned as 500

### Frontend
- Network errors: Displayed in error alert
- Empty data: Shows empty charts with zero values
- Loading states: Shows spinner during data fetch

## Testing the Complete Flow

### 1. Test Raspberry Pi Client
```bash
# On Raspberry Pi
python3 raspberry_pi_client.py
```

### 2. Verify Backend Receives Data
```bash
# Check backend logs
tail -f /tmp/airiq_backend.log

# Test endpoint
curl -X POST http://localhost:8003/api/v1/ingest \
  -H "Authorization: Bearer pi-key-1" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "RPI-TEST-01",
    "ts": "2025-11-27T22:00:00Z",
    "pm25": 15.5,
    "co2": 750,
    "temp_c": 24.1,
    "rh": 48.0
  }'
```

### 3. Verify MongoDB Storage
```bash
mongosh airiq
db.readings.find().sort({ts: -1}).limit(1).pretty()
```

### 4. Verify Frontend Display
- Open http://localhost:3000
- Check that data appears in charts
- Verify metrics show current values

## Production Considerations

1. **Security**:
   - Use HTTPS for all API calls
   - Rotate API keys regularly
   - Implement rate limiting

2. **Performance**:
   - Index MongoDB collections properly
   - Implement data aggregation for historical queries
   - Cache frequently accessed data

3. **Reliability**:
   - Set up monitoring and alerts
   - Implement data backup strategy
   - Handle sensor failures gracefully

4. **Scalability**:
   - Use connection pooling for MongoDB
   - Consider message queue for high-volume ingestion
   - Implement horizontal scaling if needed


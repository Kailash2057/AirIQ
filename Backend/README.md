# 🧠 AirIQ – Sprint 3 Backend (Detailed README)

## 🌍 Project Overview
This backend is part of the **IoT-Based Campus Air Quality Monitor (AirIQ)** project.  
It collects air-quality data from Raspberry Pi sensor nodes across the campus and provides APIs for a web dashboard to visualize the readings.

The backend:
1. Accepts data from IoT sensors (Raspberry Pi nodes)  
2. Stores readings in a local SQLite database  
3. Provides REST APIs for charts and maps  
4. Lets you update sensor metadata such as coordinates and names  

---

## ⚙️ Technologies Used
- **Python 3.11+**
- **FastAPI** – lightweight web framework for APIs  
- **SQLite + SQLAlchemy** – database and ORM  
- **Pydantic** – data validation  
- **Uvicorn** – server to run FastAPI  
- **python-dotenv** – load environment variables from `.env`

---

## 🚀 How to Run the Backend

### 1️⃣ Set up environment
```bash
python -m venv .venv
# Activate virtual env
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Create and configure `.env`
```bash
cp .env.example .env
```
Then open `.env` and review:
```bash
API_V1_PREFIX=/api/v1
DEVICE_API_KEYS=pi-key-1,pi-key-2
SQLITE_PATH=./airiq.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 4️⃣ Run the server
```bash
uvicorn app.main:app --reload --port 8000
```

Visit:
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧾 Project Folder Structure

```
airiq_sprint3_backend/
├─ README.md
├─ .env.example
├─ requirements.txt
├─ sample_client.py
└─ app/
   ├─ main.py
   ├─ db.py
   ├─ models.py
   ├─ schemas.py
   ├─ services/
   │  └─ aqi.py
   └─ routes/
      ├─ ingest.py
      ├─ sensors.py
      ├─ map_latest.py
      └─ readings.py
```

---

## 🧩 Inside the `app/` Folder

### ⚙️ `main.py`
Bootstraps FastAPI, creates DB tables, loads `.env`, and registers routers.  
Routers include: `/ingest`, `/sensors`, `/map`, `/readings`.

### 🗃️ `db.py`
Sets up SQLite connection, ORM `Base`, and `SessionLocal` for DB access.

### 🧱 `models.py`
Defines two tables:  
- **Sensor** → device info (id, name, location, status).  
- **Reading** → individual measurements (timestamped data).

### 📜 `schemas.py`
Defines Pydantic models for validation of inputs/outputs.

### 🌫️ `services/aqi.py`
Converts PM2.5 values into AQI numbers and categories.

### 🛣️ `routes/`
- **ingest.py:** `POST /api/v1/ingest` → receives and stores sensor data.  
- **sensors.py:** `GET`, `PATCH` endpoints to list and update sensors.  
- **map_latest.py:** `GET /api/v1/map/latest` → returns latest reading per sensor.  
- **readings.py:** `GET /api/v1/readings` → returns readings within time ranges for charts.

---

## 🧪 Quick Testing Commands

### Post fake reading
```bash
curl -X POST "http://localhost:8000/api/v1/ingest"   -H "Authorization: Bearer pi-key-1"   -H "Content-Type: application/json"   -d '{
    "sensor_id": "RPI-ENG-HALL-01",
    "ts": "2025-10-12T18:00:00Z",
    "pm25": 12.5, "pm10": 20.0, "co2": 750,
    "no2": 0.012, "temp_c": 24.1, "rh": 48.0,
    "battery": 95, "firmware": "1.0.0"
  }'
```

### List sensors
```bash
curl "http://localhost:8000/api/v1/sensors"
```

### Get latest per sensor for map
```bash
curl "http://localhost:8000/api/v1/map/latest"
```

### Historical readings for charts
```bash
curl "http://localhost:8000/api/v1/readings?sensor_id=RPI-ENG-HALL-01&start=2025-10-12T00:00:00Z&end=2025-10-12T23:59:59Z"
```

### Update coordinates
```bash
curl -X PATCH "http://localhost:8000/api/v1/sensors/RPI-ENG-HALL-01"   -H "Content-Type: application/json"   -d '{ "lat": 32.7313, "lon": -97.1106, "location_label": "Engineering Hall Lobby" }'
```

# MongoDB Setup Guide

## Installation

### macOS (using Homebrew)
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### Linux (Ubuntu/Debian)
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update and install
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Windows
Download and install from: https://www.mongodb.com/try/download/community

### Docker (Alternative)
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## Configuration

The backend is configured to connect to MongoDB using these environment variables in `.env`:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=airiq
```

For MongoDB Atlas (cloud), use:
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/airiq?retryWrites=true&w=majority
MONGODB_DATABASE=airiq
```

## Verify MongoDB is Running

```bash
# Check if MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Or connect to MongoDB shell
mongosh
```

## Database Structure

The backend uses two collections:

1. **sensors** - Stores sensor metadata
   - `id` (string, unique) - Sensor ID
   - `name`, `model`, `lat`, `lon`, `location_label`
   - `installed_at`, `status`

2. **readings** - Stores sensor readings
   - `sensor_id` (string) - Reference to sensor
   - `ts` (datetime) - Timestamp
   - `pm25`, `pm10`, `co2`, `no2`, `temp_c`, `rh`
   - `battery`, `firmware`, `raw_json`

## Indexes

The following indexes are automatically created:
- `sensors.id` - Unique index on sensor ID
- `readings.sensor_id` - Index for sensor lookups
- `readings.ts` - Index for time-based queries
- `readings.sensor_id + ts` - Compound index for efficient sensor+time queries

## Testing the Connection

After starting the backend, check the health endpoint:
```bash
curl http://localhost:8000/health
```

Should return:
```json
{"status": "ok", "database": "mongodb"}
```

## Troubleshooting

1. **Connection refused**: Make sure MongoDB is running
   ```bash
   brew services start mongodb-community  # macOS
   sudo systemctl start mongod           # Linux
   ```

2. **Authentication error**: Check your MongoDB URL in `.env`

3. **Database not found**: The database and collections will be created automatically on first use

4. **Port conflict**: MongoDB uses port 27017 by default. Make sure nothing else is using it.


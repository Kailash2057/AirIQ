# Raspberry Pi Setup Guide for AirIQ

## Overview

This guide explains how to set up a Raspberry Pi to collect sensor data and send it to the AirIQ backend.

## Data Flow

```
Raspberry Pi Sensors → raspberry_pi_client.py → Backend API → MongoDB → Frontend Display
```

1. **Raspberry Pi** collects data from physical sensors
2. **Client Script** sends data to backend via HTTP POST
3. **Backend** stores data in MongoDB and calculates AQI
4. **Frontend** fetches processed data and displays it

## Hardware Requirements

### Required Sensors:
- **PM2.5/PM10 Sensor**: PMS5003 (via UART/Serial)
- **CO2 Sensor**: MH-Z19B (via UART/Serial)
- **NO2 Sensor**: MQ-135 (via ADC, e.g., MCP3008)
- **Temperature/Humidity**: DHT22 (via GPIO)
- **Battery Monitor**: Optional (via ADC if battery-powered)

### Raspberry Pi Requirements:
- Raspberry Pi 3/4 or newer
- GPIO pins for sensors
- UART/Serial ports for PM and CO2 sensors
- ADC (MCP3008) for analog sensors

## Installation Steps

### 1. Install Python and Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3 python3-pip python3-venv

# Install system dependencies
sudo apt-get install -y python3-dev python3-rpi.gpio
sudo apt-get install -y i2c-tools spi-tools
```

### 2. Install Python Libraries

```bash
# Create virtual environment
python3 -m venv ~/airiq-env
source ~/airiq-env/bin/activate

# Install required packages
pip install requests RPi.GPIO
pip install adafruit-circuitpython-dht
pip install pyserial
pip install adafruit-circuitpython-mcp3xxx
```

### 3. Configure the Client Script

Edit `raspberry_pi_client.py`:

```python
# Set your backend URL
BACKEND_URL = "http://your-backend-ip:8003"

# Set your device API key (from backend .env)
DEVICE_KEY = "pi-key-1"

# Set sensor ID (single sensor)
SENSOR_ID = "AIRIQ-SENSOR-01"
```

Or use environment variables:

```bash
export AIRIQ_BACKEND_URL="http://your-backend-ip:8003"
export AIRIQ_DEVICE_KEY="pi-key-1"
export AIRIQ_SENSOR_ID="RPI-LOCATION-01"
export AIRIQ_INTERVAL="300"  # 5 minutes
```

### 4. Set Up as a System Service

Create service file:

```bash
sudo nano /etc/systemd/system/airiq-sensor.service
```

Add this content:

```ini
[Unit]
Description=AirIQ Sensor Client
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/airiq
Environment="AIRIQ_BACKEND_URL=http://your-backend-ip:8003"
Environment="AIRIQ_DEVICE_KEY=pi-key-1"
Environment="AIRIQ_SENSOR_ID=AIRIQ-SENSOR-01"
Environment="AIRIQ_INTERVAL=300"
ExecStart=/home/pi/airiq-env/bin/python3 /home/pi/airiq/raspberry_pi_client.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable airiq-sensor.service
sudo systemctl start airiq-sensor.service
sudo systemctl status airiq-sensor.service
```

### 5. View Logs

```bash
# View service logs
sudo journalctl -u airiq-sensor.service -f

# View application logs
tail -f /var/log/airiq-sensor.log
```

## Sensor Wiring Examples

### DHT22 (Temperature/Humidity)
- VCC → 3.3V
- GND → GND
- DATA → GPIO 4

### PMS5003 (PM2.5/PM10)
- VCC → 5V
- GND → GND
- RX → GPIO 15 (UART TX)
- TX → GPIO 14 (UART RX)

### MH-Z19B (CO2)
- VCC → 5V
- GND → GND
- RX → GPIO 15 (UART TX)
- TX → GPIO 14 (UART RX)

### MQ-135 (NO2) via MCP3008 ADC
- VCC → 5V
- GND → GND
- AOUT → MCP3008 CH0
- MCP3008 → SPI interface

## Testing

### Manual Test

```bash
# Activate virtual environment
source ~/airiq-env/bin/activate

# Run client script manually
python3 raspberry_pi_client.py
```

### Verify Data Reception

Check backend logs:
```bash
tail -f /tmp/airiq_backend.log
```

Check MongoDB:
```bash
mongosh airiq
db.readings.find().sort({ts: -1}).limit(5)
```

## Troubleshooting

1. **Connection refused**: Check backend URL and network connectivity
2. **401 Unauthorized**: Verify DEVICE_KEY matches backend .env
3. **Sensor not reading**: Check wiring and GPIO permissions
4. **Service not starting**: Check logs with `journalctl -u airiq-sensor.service`

## Security Notes

- Use HTTPS in production
- Rotate API keys regularly
- Use firewall rules to restrict access
- Consider VPN for remote sensors


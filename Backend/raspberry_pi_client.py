#!/usr/bin/env python3
"""
Raspberry Pi Sensor Client for AirIQ

This script runs on the Raspberry Pi and:
1. Reads sensor data from connected sensors
2. Sends data to the AirIQ backend API
3. Handles errors and retries
4. Runs continuously at specified intervals

Hardware Requirements:
- PM2.5/PM10 sensor (e.g., PMS5003)
- CO2 sensor (e.g., MH-Z19B)
- NO2 sensor (e.g., MQ-135)
- Temperature/Humidity sensor (e.g., DHT22)
- Battery monitoring (if battery-powered)

Installation on Raspberry Pi:
1. Install required libraries:
   pip install requests RPi.GPIO adafruit-circuitpython-dht
   
2. Configure this script:
   - Set BACKEND_URL to your backend server
   - Set DEVICE_KEY to your API key
   - Set SENSOR_ID to unique sensor identifier
   - Adjust sensor pin numbers as needed

3. Run as a service:
   sudo systemctl enable airiq-sensor.service
   sudo systemctl start airiq-sensor.service
"""

import time
import json
import requests
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import logging

# Configuration
BACKEND_URL = os.getenv("AIRIQ_BACKEND_URL", "http://localhost:8003")
API_ENDPOINT = f"{BACKEND_URL}/api/v1/ingest"
DEVICE_KEY = os.getenv("AIRIQ_DEVICE_KEY", "pi-key-1")
SENSOR_ID = os.getenv("AIRIQ_SENSOR_ID", "AIRIQ-SENSOR-01")  # Single sensor ID
READING_INTERVAL = int(os.getenv("AIRIQ_INTERVAL", "300"))  # 5 minutes default

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/airiq-sensor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Sensor initialization flags
SENSORS_AVAILABLE = {
    'pm25_pm10': False,
    'co2': False,
    'no2': False,
    'temp_humidity': False,
    'battery': False
}

def init_sensors():
    """Initialize all available sensors"""
    global SENSORS_AVAILABLE
    
    # Try to initialize PM2.5/PM10 sensor (PMS5003)
    try:
        import serial
        # PMS5003 typically uses serial port
        # ser = serial.Serial('/dev/ttyUSB0', 9600)
        SENSORS_AVAILABLE['pm25_pm10'] = True
        logger.info("PM2.5/PM10 sensor initialized")
    except Exception as e:
        logger.warning(f"PM2.5/PM10 sensor not available: {e}")
    
    # Try to initialize CO2 sensor (MH-Z19B)
    try:
        import serial
        # MH-Z19B uses serial port
        # co2_ser = serial.Serial('/dev/ttyAMA0', 9600)
        SENSORS_AVAILABLE['co2'] = True
        logger.info("CO2 sensor initialized")
    except Exception as e:
        logger.warning(f"CO2 sensor not available: {e}")
    
    # Try to initialize NO2 sensor (MQ-135 via ADC)
    try:
        import RPi.GPIO as GPIO
        # MQ-135 uses analog pin, requires ADC (MCP3008)
        SENSORS_AVAILABLE['no2'] = True
        logger.info("NO2 sensor initialized")
    except Exception as e:
        logger.warning(f"NO2 sensor not available: {e}")
    
    # Try to initialize DHT22 temperature/humidity sensor
    try:
        import adafruit_dht
        import board
        # dht = adafruit_dht.DHT22(board.D4)
        SENSORS_AVAILABLE['temp_humidity'] = True
        logger.info("Temperature/Humidity sensor initialized")
    except Exception as e:
        logger.warning(f"Temperature/Humidity sensor not available: {e}")
    
    # Battery monitoring (if applicable)
    try:
        import RPi.GPIO as GPIO
        # Battery voltage monitoring via ADC
        SENSORS_AVAILABLE['battery'] = True
        logger.info("Battery monitoring initialized")
    except Exception as e:
        logger.warning(f"Battery monitoring not available: {e}")

def read_pm25_pm10() -> tuple[Optional[float], Optional[float]]:
    """Read PM2.5 and PM10 values from PMS5003 sensor"""
    if not SENSORS_AVAILABLE['pm25_pm10']:
        return None, None
    
    try:
        # Example implementation for PMS5003
        # ser = serial.Serial('/dev/ttyUSB0', 9600)
        # data = ser.read(32)
        # pm25 = parse_pms5003_data(data, 'pm25')
        # pm10 = parse_pms5003_data(data, 'pm10')
        
        # For now, return mock data (replace with actual sensor reading)
        pm25 = None
        pm10 = None
        return pm25, pm10
    except Exception as e:
        logger.error(f"Error reading PM sensor: {e}")
        return None, None

def read_co2() -> Optional[float]:
    """Read CO2 value from MH-Z19B sensor"""
    if not SENSORS_AVAILABLE['co2']:
        return None
    
    try:
        # Example implementation for MH-Z19B
        # ser = serial.Serial('/dev/ttyAMA0', 9600)
        # ser.write(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79')
        # response = ser.read(9)
        # co2 = (response[2] << 8) | response[3]
        
        # For now, return mock data (replace with actual sensor reading)
        co2 = None
        return co2
    except Exception as e:
        logger.error(f"Error reading CO2 sensor: {e}")
        return None

def read_no2() -> Optional[float]:
    """Read NO2 value from MQ-135 sensor"""
    if not SENSORS_AVAILABLE['no2']:
        return None
    
    try:
        # Example implementation for MQ-135 via ADC
        # import spidev
        # spi = spidev.SpiDev()
        # spi.open(0, 0)
        # adc_value = spi.xfer2([1, (8 + 0) << 4, 0])
        # voltage = ((adc_value[1] & 3) << 8) + adc_value[2]
        # no2 = calculate_no2_from_voltage(voltage)
        
        # For now, return mock data (replace with actual sensor reading)
        no2 = None
        return no2
    except Exception as e:
        logger.error(f"Error reading NO2 sensor: {e}")
        return None

def read_temp_humidity() -> tuple[Optional[float], Optional[float]]:
    """Read temperature and humidity from DHT22 sensor"""
    if not SENSORS_AVAILABLE['temp_humidity']:
        return None, None
    
    try:
        # Example implementation for DHT22
        # import adafruit_dht
        # import board
        # dht = adafruit_dht.DHT22(board.D4)
        # temp = dht.temperature
        # humidity = dht.humidity
        
        # For now, return mock data (replace with actual sensor reading)
        temp = None
        humidity = None
        return temp, humidity
    except Exception as e:
        logger.error(f"Error reading DHT22 sensor: {e}")
        return None, None

def read_battery() -> Optional[float]:
    """Read battery percentage"""
    if not SENSORS_AVAILABLE['battery']:
        return None
    
    try:
        # Example implementation for battery monitoring
        # Read voltage from ADC and convert to percentage
        # battery_voltage = read_adc_voltage()
        # battery_percent = calculate_battery_percent(battery_voltage)
        
        # For now, return mock data (replace with actual reading)
        battery = None
        return battery
    except Exception as e:
        logger.error(f"Error reading battery: {e}")
        return None

def collect_sensor_data() -> Dict[str, Any]:
    """Collect data from all available sensors"""
    logger.info("Collecting sensor data...")
    
    # Read from all sensors
    pm25, pm10 = read_pm25_pm10()
    co2 = read_co2()
    no2 = read_no2()
    temp, humidity = read_temp_humidity()
    battery = read_battery()
    
    # Prepare payload
    payload = {
        "sensor_id": SENSOR_ID,
        "ts": datetime.now(timezone.utc).isoformat(),
        "pm25": pm25,
        "pm10": pm10,
        "co2": co2,
        "no2": no2,
        "temp_c": temp,
        "rh": humidity,
        "battery": battery,
        "firmware": "1.0.0"
    }
    
    # Log collected data
    logger.info(f"Collected data: {json.dumps(payload, indent=2)}")
    
    return payload

def send_to_backend(payload: Dict[str, Any], max_retries: int = 3) -> bool:
    """Send sensor data to backend API with retry logic"""
    headers = {
        "Authorization": f"Bearer {DEVICE_KEY}",
        "Content-Type": "application/json"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                API_ENDPOINT,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Data sent successfully: {response.json()}")
                return True
            else:
                logger.warning(f"Backend returned status {response.status_code}: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending data (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
    
    logger.error("Failed to send data after all retries")
    return False

def main_loop():
    """Main loop: collect and send data at intervals"""
    logger.info(f"Starting AirIQ sensor client")
    logger.info(f"Backend URL: {BACKEND_URL}")
    logger.info(f"Sensor ID: {SENSOR_ID}")
    logger.info(f"Reading interval: {READING_INTERVAL} seconds")
    
    init_sensors()
    
    while True:
        try:
            # Collect sensor data
            payload = collect_sensor_data()
            
            # Send to backend
            success = send_to_backend(payload)
            
            if success:
                logger.info(f"Waiting {READING_INTERVAL} seconds until next reading...")
            else:
                logger.warning("Failed to send data, will retry on next cycle")
            
            # Wait for next reading
            time.sleep(READING_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            time.sleep(READING_INTERVAL)

if __name__ == "__main__":
    main_loop()


#A simple helper that turns PM2.5 values into AQI numbers and categories:
#  Minimal PM2.5 AQI mapping (placeholder; replace with full EPA table as needed)
def pm25_to_aqi(pm25: float | None) -> tuple[int | None, str | None]:
    if pm25 is None:
        return None, None
    if pm25 <= 12.0:
        return 50, "Good"
    if pm25 <= 35.4:
        return 100, "Moderate"
    if pm25 <= 55.4:
        return 150, "USG"
    if pm25 <= 150.4:
        return 200, "Unhealthy"
    if pm25 <= 250.4:
        return 300, "Very Unhealthy"
    return 400, "Hazardous"

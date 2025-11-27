'''
Purpose: provides historical data for charts.

Query parameters:

Parameter	Description
sensor_id	filter by sensor
start	ISO datetime (inclusive)
end	ISO datetime (inclusive)
limit	max number of rows (default 5000, max 20000)
'''

from fastapi import APIRouter, Query
from datetime import datetime
from ..models import Reading
from ..schemas import ReadingOut
from typing import Optional

router = APIRouter(prefix="/readings", tags=["readings"])

@router.get("", response_model=list[ReadingOut])
async def time_range(
    sensor_id: Optional[str] = Query(None, description="Filter by sensor id"),
    start: Optional[datetime] = Query(None, description="ISO8601 start (inclusive)"),
    end: Optional[datetime] = Query(None, description="ISO8601 end (inclusive)"),
    limit: int = Query(5000, ge=1, le=20000, description="Max rows")
):
    # Build query using Beanie's query builder
    find_query = Reading.find()
    
    # Apply filters
    if sensor_id:
        find_query = find_query.find(Reading.sensor_id == sensor_id)
    
    if start:
        find_query = find_query.find(Reading.ts >= start)
    
    if end:
        find_query = find_query.find(Reading.ts <= end)
    
    # Execute query - sort by timestamp ascending, limit results
    readings = await find_query.sort("+ts").limit(limit).to_list()
    
    return [
        ReadingOut(
            sensor_id=r.sensor_id,
            ts=r.ts,
            pm25=r.pm25,
            pm10=r.pm10,
            co2=r.co2,
            no2=r.no2,
            temp_c=r.temp_c,
            rh=r.rh,
            battery=r.battery,
            firmware=r.firmware
        ) for r in readings
    ]

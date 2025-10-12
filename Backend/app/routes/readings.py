'''
Purpose: provides historical data for charts.

Query parameters:

Parameter	Description
sensor_id	filter by sensor
start	ISO datetime (inclusive)
end	ISO datetime (inclusive)
limit	max number of rows (default 5000, max 20000)
'''


from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from datetime import datetime
from ..db import get_db
from ..models import Reading
from ..schemas import ReadingOut

router = APIRouter(prefix="/readings", tags=["readings"])

@router.get("", response_model=list[ReadingOut])
def time_range(
    sensor_id: str | None = Query(None, description="Filter by sensor id"),
    start: datetime | None = Query(None, description="ISO8601 start (inclusive)"),
    end: datetime | None = Query(None, description="ISO8601 end (inclusive)"),
    limit: int = Query(5000, ge=1, le=20000, description="Max rows")
    , db: Session = Depends(get_db),
):
    conds = []
    if sensor_id:
        conds.append(Reading.sensor_id == sensor_id)
    if start:
        conds.append(Reading.ts >= start)
    if end:
        conds.append(Reading.ts <= end)
    stmt = select(Reading).where(and_(*conds)) if conds else select(Reading)
    stmt = stmt.order_by(Reading.ts.asc()).limit(limit)
    rows = db.scalars(stmt).all()
    return [
        ReadingOut(
            sensor_id=r.sensor_id,
            ts=r.ts,
            pm25=r.pm25, pm10=r.pm10, co2=r.co2, no2=r.no2,
            temp_c=r.temp_c, rh=r.rh, battery=r.battery, firmware=r.firmware
        ) for r in rows
    ]

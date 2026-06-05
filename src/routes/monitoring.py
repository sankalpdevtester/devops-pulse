"""Monitoring routes"""

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import aiohttp
import time

from ..database import get_db
from ..models import Endpoint, MonitoringResult
from ..schemas import MonitoringResultSchema, EndpointHealthSchema

router = APIRouter()

@router.get("/check/{endpoint_id}", response_model=MonitoringResultSchema)
async def check_endpoint(
    endpoint_id: int,
    db: Session = Depends(get_db)
):
    """Manually trigger endpoint check"""
    endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    
    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    result = await perform_check(endpoint)
    
    # Save result
    monitoring_result = MonitoringResult(
        endpoint_id=endpoint.id,
        status_code=result["status_code"],
        response_time=result["response_time"],
        is_up=result["is_up"],
        error_message=result.get("error")
    )
    db.add(monitoring_result)
    
    # Update endpoint stats
    endpoint.last_check = time.time()
    endpoint.last_status_code = result["status_code"]
    endpoint.last_response_time = result["response_time"]
    endpoint.is_up = result["is_up"]
    
    if not result["is_up"]:
        endpoint.consecutive_failures += 1
    else:
        endpoint.consecutive_failures = 0
    
    db.commit()
    db.refresh(monitoring_result)
    
    return monitoring_result

@router.get("/history/{endpoint_id}", response_model=List[MonitoringResultSchema])
def get_endpoint_history(
    endpoint_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get monitoring history for an endpoint"""
    results = db.query(MonitoringResult)\
        .filter(MonitoringResult.endpoint_id == endpoint_id)\
        .order_by(MonitoringResult.timestamp.desc())\
        .limit(limit)\
        .all()
    
    return results

@router.get("/health", response_model=List[EndpointHealthSchema])
def get_all_endpoints_health(db: Session = Depends(get_db)):
    """Get health status of all endpoints"""
    endpoints = db.query(Endpoint).all()
    
    return [
        {
            "id": ep.id,
            "name": ep.name,
            "url": ep.url,
            "is_up": ep.is_up,
            "last_check": ep.last_check,
            "last_response_time": ep.last_response_time,
            "consecutive_failures": ep.consecutive_failures
        }
        for ep in endpoints
    ]

async def perform_check(endpoint: Endpoint) -> dict:
    """Perform actual HTTP check"""
    result = {
        "status_code": None,
        "response_time": None,
        "is_up": False,
        "error": None
    }
    
    start_time = time.time()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=endpoint.method,
                url=endpoint.url,
                timeout=aiohttp.ClientTimeout(total=endpoint.timeout)
            ) as response:
                result["status_code"] = response.status
                result["response_time"] = (time.time() - start_time) * 1000  # ms
                result["is_up"] = 200 <= response.status < 500
                
    except asyncio.TimeoutError:
        result["error"] = "Request timeout"
        result["response_time"] = (time.time() - start_time) * 1000
    except Exception as e:
        result["error"] = str(e)
        result["response_time"] = (time.time() - start_time) * 1000
    
    return result

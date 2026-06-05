"""Dashboard routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import Endpoint, MonitoringResult
from ..schemas import DashboardStatsSchema

router = APIRouter()

@router.get("/stats", response_model=DashboardStatsSchema)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get aggregated dashboard statistics"""
    
    # Total endpoints
    total_endpoints = db.query(func.count(Endpoint.id)).scalar()
    
    # Active endpoints (up)
    active_endpoints = db.query(func.count(Endpoint.id))\
        .filter(Endpoint.is_up == True)\
        .scalar()
    
    # Failing endpoints
    failing_endpoints = total_endpoints - active_endpoints
    
    # Average response time (last 100 checks)
    avg_response = db.query(func.avg(MonitoringResult.response_time))\
        .limit(100)\
        .scalar()
    
    # Uptime percentage (last 24h)
    total_checks = db.query(func.count(MonitoringResult.id)).scalar()
    successful_checks = db.query(func.count(MonitoringResult.id))\
        .filter(MonitoringResult.is_up == True)\
        .scalar()
    
    uptime_percent = (successful_checks / total_checks * 100) if total_checks > 0 else 100.0
    
    return {
        "total_endpoints": total_endpoints,
        "active_endpoints": active_endpoints,
        "failing_endpoints": failing_endpoints,
        "avg_response_time": round(avg_response, 2) if avg_response else 0,
        "uptime_percent": round(uptime_percent, 2)
    }

@router.get("/activity")
def get_recent_activity(limit: int = 20, db: Session = Depends(get_db)):
    """Get recent monitoring activity"""
    
    results = db.query(MonitoringResult)\
        .join(Endpoint)\
        .order_by(MonitoringResult.timestamp.desc())\
        .limit(limit)\
        .all()
    
    activity = []
    for result in results:
        activity.append({
            "endpoint_name": result.endpoint.name,
            "endpoint_url": result.endpoint.url,
            "status": "up" if result.is_up else "down",
            "status_code": result.status_code,
            "response_time": result.response_time,
            "timestamp": result.timestamp,
            "error": result.error_message
        })
    
    return activity

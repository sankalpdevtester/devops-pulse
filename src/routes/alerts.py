"""Alert routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Alert
from ..schemas import AlertSchema, AlertCreateSchema

router = APIRouter()

@router.get("/", response_model=List[AlertSchema])
def list_alerts(
    status: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all alerts"""
    query = db.query(Alert)
    
    if status:
        query = query.filter(Alert.status == status)
    
    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
    return alerts

@router.post("/", response_model=AlertSchema)
def create_alert(
    alert: AlertCreateSchema,
    db: Session = Depends(get_db)
):
    """Create a new alert"""
    db_alert = Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.patch("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """Acknowledge an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = "acknowledged"
    db.commit()
    
    return {"message": "Alert acknowledged"}

@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """Delete an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(alert)
    db.commit()
    
    return {"message": "Alert deleted"}

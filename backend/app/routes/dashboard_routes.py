
"""
Dashboard routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Device, Rule, Incident, PlaybookExecution, User
from ..schemas import DashboardMetrics, DeviceStatusSummary
from ..auth import get_current_user
from typing import List

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard metrics
    """
    # Count incidents by status
    active_incidents = db.query(func.count(Incident.incident_id)).filter(
        Incident.status.in_(["open", "investigating"])
    ).scalar() or 0
    
    open_investigations = db.query(func.count(Incident.incident_id)).filter(
        Incident.status == "investigating"
    ).scalar() or 0
    
    # Count playbook executions in last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    playbook_executions_24h = db.query(func.count(PlaybookExecution.execution_id)).filter(
        PlaybookExecution.created_at >= yesterday
    ).scalar() or 0
    
    # Device health
    devices = db.query(Device).all()
    device_health = {
        "connected": sum(1 for d in devices if d.connection_status == "connected"),
        "disconnected": sum(1 for d in devices if d.connection_status == "disconnected"),
        "error": sum(1 for d in devices if d.connection_status == "error")
    }
    
    # Incidents by severity
    incidents_by_severity = {
        "critical": db.query(func.count(Incident.incident_id)).filter(
            Incident.severity == "Critical"
        ).scalar() or 0,
        "high": db.query(func.count(Incident.incident_id)).filter(
            Incident.severity == "High"
        ).scalar() or 0,
        "medium": db.query(func.count(Incident.incident_id)).filter(
            Incident.severity == "Medium"
        ).scalar() or 0,
        "low": db.query(func.count(Incident.incident_id)).filter(
            Incident.severity == "Low"
        ).scalar() or 0
    }
    
    # Mock MTTI/MTTDA for now (can be calculated from real incident data)
    mtti_average_minutes = 4.2
    mttda_average_minutes = 6.8
    
    return DashboardMetrics(
        active_incidents=active_incidents,
        open_investigations=open_investigations,
        playbook_executions_24h=playbook_executions_24h,
        mtti_average_minutes=mtti_average_minutes,
        mttda_average_minutes=mttda_average_minutes,
        device_health=device_health,
        incidents_by_severity=incidents_by_severity
    )


@router.get("/device-health", response_model=List[DeviceStatusSummary])
async def get_device_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get device health status summary
    """
    devices = db.query(Device).all()
    
    response = []
    for device in devices:
        rules_count = db.query(func.count(Rule.id)).filter(Rule.device_id == device.id).scalar() or 0
        
        response.append(DeviceStatusSummary(
            id=device.id,
            name=device.name,
            type=device.type,
            status=device.connection_status,
            last_tested=device.last_tested,
            rules_count=rules_count
        ))
    
    return response

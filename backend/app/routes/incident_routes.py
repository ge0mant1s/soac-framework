"""
Incident Management API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List, Optional
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Incident
from ..auth import get_current_user
from ..playbooks.playbook_executor import PlaybookExecutor
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.get("/")
def list_incidents(
    status: Optional[str] = Query(None, description="Filter by status"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    pattern_id: Optional[str] = Query(None, description="Filter by pattern ID"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned analyst"),
    days: Optional[int] = Query(7, description="Number of days to look back"),
    limit: Optional[int] = Query(100, description="Maximum number of incidents to return"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    List incidents with optional filters
    """
    try:
        query = db.query(Incident)
        
        # Apply filters
        filters = []
        
        if status:
            filters.append(Incident.status == status)
        
        if severity:
            filters.append(Incident.severity == severity)
        
        if pattern_id:
            filters.append(Incident.pattern_id == pattern_id)
        
        if assigned_to:
            filters.append(Incident.assigned_to == assigned_to)
        
        # Date filter
        if days:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            filters.append(Incident.created_at >= cutoff_date)
        
        if filters:
            query = query.filter(and_(*filters))
        
        # Order by created_at descending and limit
        incidents = query.order_by(desc(Incident.created_at)).limit(limit).all()
        
        return {
            "incidents": [
                {
                    "incident_id": inc.incident_id,
                    "pattern_id": inc.pattern_id,
                    "pattern_name": inc.pattern_name,
                    "entity_key": inc.entity_key,
                    "phases_matched": inc.phases_matched,
                    "confidence_level": inc.confidence_level,
                    "event_count": inc.event_count,
                    "severity": inc.severity,
                    "status": inc.status,
                    "assigned_to": inc.assigned_to,
                    "created_at": inc.created_at.isoformat(),
                    "updated_at": inc.updated_at.isoformat()
                }
                for inc in incidents
            ],
            "total": len(incidents)
        }
    except Exception as e:
        logger.error(f"Error listing incidents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{incident_id}")
def get_incident(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed information about a specific incident
    """
    try:
        incident = db.query(Incident).filter_by(incident_id=incident_id).first()
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        return {
            "incident_id": incident.incident_id,
            "pattern_id": incident.pattern_id,
            "pattern_name": incident.pattern_name,
            "entity_key": incident.entity_key,
            "phases_matched": incident.phases_matched,
            "confidence_level": incident.confidence_level,
            "event_count": incident.event_count,
            "events": incident.events,
            "severity": incident.severity,
            "status": incident.status,
            "assigned_to": incident.assigned_to,
            "created_at": incident.created_at.isoformat(),
            "updated_at": incident.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting incident {incident_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{incident_id}")
def update_incident(
    incident_id: str,
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update incident status or assignment
    """
    try:
        incident = db.query(Incident).filter_by(incident_id=incident_id).first()
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        # Update fields
        if status:
            valid_statuses = ["open", "investigating", "contained", "resolved", "false_positive"]
            if status not in valid_statuses:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                )
            incident.status = status
        
        if assigned_to is not None:  # Allow empty string to unassign
            incident.assigned_to = assigned_to
        
        incident.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Updated incident {incident_id}: status={status}, assigned_to={assigned_to}")
        
        return {
            "message": "Incident updated successfully",
            "incident_id": incident.incident_id,
            "status": incident.status,
            "assigned_to": incident.assigned_to
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating incident {incident_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{incident_id}/assign")
def assign_incident(
    incident_id: str,
    analyst: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Assign incident to an analyst
    """
    try:
        incident = db.query(Incident).filter_by(incident_id=incident_id).first()
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        incident.assigned_to = analyst
        incident.updated_at = datetime.utcnow()
        
        # Also update status to investigating if it's open
        if incident.status == "open":
            incident.status = "investigating"
        
        db.commit()
        
        logger.info(f"Assigned incident {incident_id} to {analyst}")
        
        return {
            "message": f"Incident assigned to {analyst}",
            "incident_id": incident.incident_id,
            "assigned_to": incident.assigned_to,
            "status": incident.status
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning incident {incident_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{incident_id}/execute-playbook")
def execute_playbook_for_incident(
    incident_id: str,
    playbook_id: Optional[str] = None,
    mode: str = "manual",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Execute a playbook for an incident
    If playbook_id is not provided, execute all relevant playbooks based on decision matrix
    """
    try:
        # Check incident exists
        incident = db.query(Incident).filter_by(incident_id=incident_id).first()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        executor = PlaybookExecutor(db)
        
        if playbook_id:
            # Execute specific playbook
            result = executor.execute_playbook(
                playbook_id=playbook_id,
                incident_id=incident_id,
                mode=mode
            )
            return result
        else:
            # Execute all relevant playbooks
            results = executor.execute_playbooks_for_incident(
                incident_id=incident_id,
                mode=mode
            )
            return {
                "message": f"Executed {len(results)} playbooks",
                "executions": results
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing playbook for incident {incident_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{incident_id}/playbooks")
def get_incident_playbooks(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get playbook executions for an incident
    """
    try:
        executor = PlaybookExecutor(db)
        executions = executor.list_executions(incident_id=incident_id)
        
        return {
            "incident_id": incident_id,
            "executions": executions,
            "total": len(executions)
        }
    except Exception as e:
        logger.error(f"Error getting playbooks for incident {incident_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
def get_incident_stats(
    days: Optional[int] = Query(7, description="Number of days to look back"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get incident statistics summary
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Total incidents
        total_incidents = db.query(Incident).filter(
            Incident.created_at >= cutoff_date
        ).count()
        
        # By status
        status_counts = {}
        for status in ["open", "investigating", "contained", "resolved", "false_positive"]:
            count = db.query(Incident).filter(
                and_(
                    Incident.status == status,
                    Incident.created_at >= cutoff_date
                )
            ).count()
            status_counts[status] = count
        
        # By severity
        severity_counts = {}
        for severity in ["Critical", "High", "Medium", "Low"]:
            count = db.query(Incident).filter(
                and_(
                    Incident.severity == severity,
                    Incident.created_at >= cutoff_date
                )
            ).count()
            severity_counts[severity] = count
        
        # Recent incidents (last 24 hours)
        recent_cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_count = db.query(Incident).filter(
            Incident.created_at >= recent_cutoff
        ).count()
        
        return {
            "total_incidents": total_incidents,
            "recent_incidents_24h": recent_count,
            "by_status": status_counts,
            "by_severity": severity_counts,
            "period_days": days
        }
    except Exception as e:
        logger.error(f"Error getting incident stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

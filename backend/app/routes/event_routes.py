"""
Event management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Event, Device, User
from ..schemas import (
    EventResponse, EventListResponse, EventStatsResponse,
    EventCollectionRequest, EventCollectionResponse
)
from ..auth import get_current_user
from ..services.event_ingestion import event_ingestion_service

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=EventListResponse)
async def list_events(
    device_id: Optional[UUID] = Query(None, description="Filter by device ID"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    start_time: Optional[datetime] = Query(None, description="Start time filter"),
    end_time: Optional[datetime] = Query(None, description="End time filter"),
    processed: Optional[bool] = Query(None, description="Filter by processed status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=500, description="Page size"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of events with filtering and pagination
    """
    # Build query
    query = db.query(Event)
    
    # Apply filters
    filters = []
    
    if device_id:
        filters.append(Event.device_id == device_id)
    
    if event_type:
        filters.append(Event.event_type == event_type)
    
    if severity:
        filters.append(Event.severity == severity)
    
    if start_time:
        filters.append(Event.timestamp >= start_time)
    
    if end_time:
        filters.append(Event.timestamp <= end_time)
    
    if processed is not None:
        filters.append(Event.processed == processed)
    
    if filters:
        query = query.filter(and_(*filters))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    events = query.order_by(desc(Event.timestamp)).offset(offset).limit(page_size).all()
    
    # Convert to response models
    event_responses = []
    for event in events:
        event_responses.append(EventResponse(
            id=event.id,
            device_id=event.device_id,
            timestamp=event.timestamp,
            event_type=event.event_type,
            severity=event.severity,
            raw_data=event.raw_data,
            normalized_data=event.normalized_data,
            processed=event.processed,
            detection_results=event.detection_results,
            created_at=event.created_at
        ))
    
    return EventListResponse(
        total=total,
        events=event_responses,
        page=page,
        page_size=page_size
    )


@router.get("/stats", response_model=EventStatsResponse)
async def get_event_stats(
    device_id: Optional[UUID] = Query(None, description="Filter by device ID"),
    hours: int = Query(24, ge=1, le=720, description="Hours to look back"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get event statistics
    """
    # Build base query
    start_time = datetime.utcnow() - timedelta(hours=hours)
    query = db.query(Event).filter(Event.timestamp >= start_time)
    
    if device_id:
        query = query.filter(Event.device_id == device_id)
    
    # Total events
    total_events = query.count()
    
    # Events by type
    events_by_type = {}
    type_results = db.query(Event.event_type, func.count(Event.id)).filter(
        Event.timestamp >= start_time
    )
    if device_id:
        type_results = type_results.filter(Event.device_id == device_id)
    
    for event_type, count in type_results.group_by(Event.event_type).all():
        if event_type:
            events_by_type[event_type] = count
    
    # Events by severity
    events_by_severity = {}
    severity_results = db.query(Event.severity, func.count(Event.id)).filter(
        Event.timestamp >= start_time
    )
    if device_id:
        severity_results = severity_results.filter(Event.device_id == device_id)
    
    for severity, count in severity_results.group_by(Event.severity).all():
        if severity:
            events_by_severity[severity] = count
    
    # Events by device
    events_by_device = {}
    if not device_id:
        device_results = db.query(Device.name, func.count(Event.id)).join(
            Event, Device.id == Event.device_id
        ).filter(Event.timestamp >= start_time).group_by(Device.name).all()
        
        for device_name, count in device_results:
            events_by_device[device_name] = count
    
    # Processed vs unprocessed
    processed_events = query.filter(Event.processed == True).count()
    unprocessed_events = total_events - processed_events
    
    return EventStatsResponse(
        total_events=total_events,
        events_by_type=events_by_type,
        events_by_severity=events_by_severity,
        events_by_device=events_by_device,
        processed_events=processed_events,
        unprocessed_events=unprocessed_events
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific event by ID
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return EventResponse(
        id=event.id,
        device_id=event.device_id,
        timestamp=event.timestamp,
        event_type=event.event_type,
        severity=event.severity,
        raw_data=event.raw_data,
        normalized_data=event.normalized_data,
        processed=event.processed,
        detection_results=event.detection_results,
        created_at=event.created_at
    )


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific event
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.delete(event)
    db.commit()
    
    return None


@router.post("/collect", response_model=EventCollectionResponse)
async def collect_events_all_devices(
    request: EventCollectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually trigger event collection from all enabled devices
    """
    devices = db.query(Device).filter(Device.enabled == True).all()
    
    if not devices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No enabled devices found"
        )
    
    total_collected = 0
    total_stored = 0
    errors = []
    
    for device in devices:
        result = event_ingestion_service.manual_collect(
            device_id=str(device.id),
            db=db,
            hours=request.hours,
            limit=request.limit
        )
        
        if result.get("success"):
            total_collected += result.get("events_collected", 0)
            total_stored += result.get("events_stored", 0)
        else:
            errors.append(f"{device.name}: {result.get('error', 'Unknown error')}")
    
    message = f"Collected {total_stored} events from {len(devices)} devices"
    if errors:
        message += f". Errors: {'; '.join(errors)}"
    
    return EventCollectionResponse(
        success=len(errors) == 0,
        device_id="all",
        events_collected=total_collected,
        events_stored=total_stored,
        message=message
    )

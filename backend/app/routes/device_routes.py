
"""
Device management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from uuid import UUID
from datetime import datetime
from ..database import get_db
from ..models import Device, Rule, User
from ..schemas import (
    DeviceCreate, DeviceUpdate, DeviceResponse, 
    ConnectionTestResponse, SyncResponse, HealthResponse
)
from ..auth import get_current_user
from ..services.sync_service import SyncService

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("", response_model=List[DeviceResponse])
async def list_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all devices with rules count
    """
    devices = db.query(Device).all()
    
    response = []
    for device in devices:
        rules_count = db.query(func.count(Rule.id)).filter(Rule.device_id == device.id).scalar()
        device_dict = {
            "id": device.id,
            "name": device.name,
            "type": device.type,
            "enabled": device.enabled,
            "config": device.config,
            "connection_status": device.connection_status,
            "last_tested": device.last_tested,
            "last_sync": device.last_sync,
            "rules_count": rules_count or 0,
            "created_at": device.created_at,
            "updated_at": device.updated_at
        }
        response.append(DeviceResponse(**device_dict))
    
    return response


@router.post("", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new device integration
    """
    # Validate device type
    valid_types = ["paloalto", "entraid", "siem"]
    if device_data.type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid device type. Must be one of: {', '.join(valid_types)}"
        )
    
    # Create device
    device = Device(
        name=device_data.name,
        type=device_data.type,
        enabled=device_data.enabled,
        config=device_data.config,
        connection_status="disconnected"
    )
    
    db.add(device)
    db.commit()
    db.refresh(device)
    
    device_dict = {
        "id": device.id,
        "name": device.name,
        "type": device.type,
        "enabled": device.enabled,
        "config": device.config,
        "connection_status": device.connection_status,
        "last_tested": device.last_tested,
        "last_sync": device.last_sync,
        "rules_count": 0,
        "created_at": device.created_at,
        "updated_at": device.updated_at
    }
    
    return DeviceResponse(**device_dict)


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific device by ID
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    rules_count = db.query(func.count(Rule.id)).filter(Rule.device_id == device.id).scalar()
    
    device_dict = {
        "id": device.id,
        "name": device.name,
        "type": device.type,
        "enabled": device.enabled,
        "config": device.config,
        "connection_status": device.connection_status,
        "last_tested": device.last_tested,
        "last_sync": device.last_sync,
        "rules_count": rules_count or 0,
        "created_at": device.created_at,
        "updated_at": device.updated_at
    }
    
    return DeviceResponse(**device_dict)


@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: UUID,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a device
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    # Update fields
    if device_data.name is not None:
        device.name = device_data.name
    if device_data.enabled is not None:
        device.enabled = device_data.enabled
    if device_data.config is not None:
        device.config = device_data.config
    
    device.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(device)
    
    rules_count = db.query(func.count(Rule.id)).filter(Rule.device_id == device.id).scalar()
    
    device_dict = {
        "id": device.id,
        "name": device.name,
        "type": device.type,
        "enabled": device.enabled,
        "config": device.config,
        "connection_status": device.connection_status,
        "last_tested": device.last_tested,
        "last_sync": device.last_sync,
        "rules_count": rules_count or 0,
        "created_at": device.created_at,
        "updated_at": device.updated_at
    }
    
    return DeviceResponse(**device_dict)


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a device
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    db.delete(device)
    db.commit()
    
    return None


@router.post("/{device_id}/test", response_model=ConnectionTestResponse)
async def test_device_connection(
    device_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Test device connection with real API integration
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    # Test connection using real implementation
    result = SyncService.test_device_connection(device.type, device.config)
    
    # Update device status
    device.connection_status = "connected" if result["success"] else "error"
    device.last_tested = datetime.utcnow()
    db.commit()
    
    return ConnectionTestResponse(**result)


@router.post("/{device_id}/sync", response_model=SyncResponse)
async def sync_device(
    device_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Sync configuration and rules from device
    Fetches rules from the device and updates database
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    if not device.enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device is disabled. Enable it before syncing."
        )
    
    # Perform sync
    result = SyncService.sync_device(device, db)
    
    return SyncResponse(**result)


@router.get("/{device_id}/health", response_model=HealthResponse)
async def get_device_health(
    device_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get device health metrics
    Returns real-time health information from the device
    """
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    # Get health metrics
    result = SyncService.get_device_health(device)
    
    return HealthResponse(**result)

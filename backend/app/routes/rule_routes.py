
"""
Rule management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..database import get_db
from ..models import Rule, Device, User
from ..schemas import RuleCreate, RuleUpdate, RuleResponse
from ..auth import get_current_user

router = APIRouter(prefix="/rules", tags=["Rules"])


@router.get("", response_model=List[RuleResponse])
async def list_rules(
    device_id: Optional[UUID] = Query(None),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all rules with optional filtering
    """
    query = db.query(Rule)
    
    if device_id:
        query = query.filter(Rule.device_id == device_id)
    if severity:
        query = query.filter(Rule.severity == severity)
    if status:
        query = query.filter(Rule.status == status)
    
    rules = query.all()
    return rules


@router.post("", response_model=RuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(
    rule_data: RuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new detection rule
    """
    # Verify device exists
    device = db.query(Device).filter(Device.id == rule_data.device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    # Check if rule ID already exists
    existing_rule = db.query(Rule).filter(Rule.id == rule_data.id).first()
    if existing_rule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rule with ID {rule_data.id} already exists"
        )
    
    # Create rule
    rule = Rule(**rule_data.model_dump())
    
    db.add(rule)
    db.commit()
    db.refresh(rule)
    
    return rule


@router.get("/{rule_id}", response_model=RuleResponse)
async def get_rule(
    rule_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific rule by ID
    """
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    return rule


@router.put("/{rule_id}", response_model=RuleResponse)
async def update_rule(
    rule_id: str,
    rule_data: RuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a rule
    """
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    # Update fields
    update_data = rule_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule, field, value)
    
    rule.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(rule)
    
    return rule


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(
    rule_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a rule
    """
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    db.delete(rule)
    db.commit()
    
    return None


@router.patch("/{rule_id}/status")
async def toggle_rule_status(
    rule_id: str,
    enabled: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Enable or disable a rule
    """
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    rule.enabled = enabled
    rule.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(rule)
    
    return {"message": f"Rule {'enabled' if enabled else 'disabled'} successfully"}

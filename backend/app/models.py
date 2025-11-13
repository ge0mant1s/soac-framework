
"""
SQLAlchemy database models
"""
from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="analyst")  # admin, analyst, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Device(Base):
    """Device integration model"""
    __tablename__ = "devices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # paloalto, entraid, siem
    enabled = Column(Boolean, default=True)
    config = Column(JSON, nullable=False)  # Encrypted credentials and connection details
    connection_status = Column(String(20), default="disconnected")  # connected, disconnected, error
    last_tested = Column(DateTime, nullable=True)
    last_sync = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rules = relationship("Rule", back_populates="device", cascade="all, delete-orphan")


class Rule(Base):
    """Detection rule model"""
    __tablename__ = "rules"
    
    id = Column(String(50), primary_key=True)  # e.g., ENTRAID-001
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False)
    use_case_id = Column(String(50), nullable=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    incident_rule = Column(Text, nullable=True)
    severity = Column(String(20), nullable=False)  # Critical, High, Medium, Low
    mitre_tactic = Column(String(100), nullable=True)
    mitre_technique = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)
    query = Column(Text, nullable=False)
    enabled = Column(Boolean, default=True)
    status = Column(String(20), default="draft")  # draft, testing, active, disabled
    false_positive_rate = Column(Float, nullable=True)
    detection_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    device = relationship("Device", back_populates="rules")


class Incident(Base):
    """Incident model"""
    __tablename__ = "incidents"
    
    incident_id = Column(String(50), primary_key=True)
    pattern_id = Column(String(10), nullable=False, index=True)
    pattern_name = Column(String(100), nullable=True)
    entity_key = Column(String(500), nullable=True, index=True)
    phases_matched = Column(JSON, nullable=True)
    confidence_level = Column(String(20), nullable=True)
    event_count = Column(Integer, default=0)
    events = Column(JSON, nullable=True)
    severity = Column(String(20), nullable=True, index=True)
    status = Column(String(50), default="open", index=True)  # open, investigating, contained, resolved, false_positive
    assigned_to = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PlaybookExecution(Base):
    """Playbook execution model"""
    __tablename__ = "playbook_executions"
    
    execution_id = Column(String(50), primary_key=True)
    incident_id = Column(String(50), ForeignKey("incidents.incident_id"), nullable=True, index=True)
    playbook_id = Column(String(50), nullable=False, index=True)
    playbook_name = Column(String(200), nullable=True)
    status = Column(String(50), nullable=True, index=True)  # pending, running, completed, failed
    steps_completed = Column(Integer, default=0)
    steps_total = Column(Integer, default=0)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


# ============= User Schemas =============

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "analyst"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Auth Schemas =============

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class LoginRequest(BaseModel):
    username: str
    password: str


# ============= Device Schemas =============

class DeviceBase(BaseModel):
    name: str
    type: str  # paloalto, entraid, siem
    enabled: bool = True
    config: Dict[str, Any]


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    enabled: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None


class DeviceResponse(DeviceBase):
    id: UUID
    connection_status: str
    last_tested: Optional[datetime] = None
    last_sync: Optional[datetime] = None
    last_connected: Optional[datetime] = None
    health_status: str = "unknown"
    event_count: int = 0
    rules_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConnectionTestResponse(BaseModel):
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None


class SyncResponse(BaseModel):
    """Response model for device sync operations"""
    success: bool
    message: str
    rules_synced: int = 0
    rules_created: int = 0
    rules_updated: int = 0
    last_sync: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for device health checks"""
    success: bool
    message: str
    health: Dict[str, Any] = {}


# ============= Rule Schemas =============

class RuleBase(BaseModel):
    id: str
    device_id: UUID
    use_case_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    incident_rule: Optional[str] = None
    severity: str
    mitre_tactic: Optional[str] = None
    mitre_technique: Optional[str] = None
    category: Optional[str] = None
    query: str
    enabled: bool = True
    status: str = "draft"


class RuleCreate(RuleBase):
    pass


class RuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    incident_rule: Optional[str] = None
    severity: Optional[str] = None
    mitre_tactic: Optional[str] = None
    mitre_technique: Optional[str] = None
    category: Optional[str] = None
    query: Optional[str] = None
    enabled: Optional[bool] = None
    status: Optional[str] = None


class RuleResponse(RuleBase):
    false_positive_rate: Optional[float] = None
    detection_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============= Dashboard Schemas =============

class DashboardMetrics(BaseModel):
    active_incidents: int = 0
    open_investigations: int = 0
    playbook_executions_24h: int = 0
    mtti_average_minutes: float = 0.0
    mttda_average_minutes: float = 0.0
    device_health: Dict[str, int] = {"connected": 0, "disconnected": 0, "error": 0}
    incidents_by_severity: Dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}


class DeviceStatusSummary(BaseModel):
    id: UUID
    name: str
    type: str
    status: str
    last_tested: Optional[datetime] = None
    rules_count: int = 0


# ============= Response Wrapper =============

class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    success: bool = False
    error: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============= Event Schemas =============

class EventBase(BaseModel):
    device_id: UUID
    timestamp: datetime
    event_type: Optional[str] = None
    severity: Optional[str] = None
    raw_data: Dict[str, Any]
    normalized_data: Optional[Dict[str, Any]] = None


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: UUID
    processed: bool = False
    detection_results: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """Response model for event listing with pagination"""
    total: int
    events: List[EventResponse]
    page: int = 1
    page_size: int = 50


class EventCollectionRequest(BaseModel):
    """Request model for manual event collection"""
    hours: int = 24
    limit: int = 500


class EventCollectionResponse(BaseModel):
    """Response model for event collection"""
    success: bool
    device_id: str
    events_collected: int = 0
    events_stored: int = 0
    message: Optional[str] = None
    error: Optional[str] = None


class EventStatsResponse(BaseModel):
    """Response model for event statistics"""
    total_events: int = 0
    events_by_type: Dict[str, int] = {}
    events_by_severity: Dict[str, int] = {}
    events_by_device: Dict[str, int] = {}
    processed_events: int = 0
    unprocessed_events: int = 0


class EventFilterParams(BaseModel):
    """Query parameters for filtering events"""
    device_id: Optional[UUID] = None
    event_type: Optional[str] = None
    severity: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    processed: Optional[bool] = None
    page: int = 1
    page_size: int = 50

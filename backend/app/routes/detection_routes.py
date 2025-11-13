
"""
Detection Engine API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from ..database import get_db
from ..auth import get_current_user
from ..detection.detection_engine import DetectionEngine
from ..detection.event_processor import EventProcessor
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/detection", tags=["Detection"])


class EventInput(BaseModel):
    """Input model for processing events"""
    event: Dict[str, Any]
    source: str  # paloalto, entraid, falcon, siem


class BatchEventInput(BaseModel):
    """Input model for processing batch events"""
    events: List[Dict[str, Any]]
    source: str


# Global detection engine instance (in production, use dependency injection)
_detection_engine = None


def get_detection_engine(db: Session = Depends(get_db)) -> DetectionEngine:
    """Get or create detection engine instance"""
    global _detection_engine
    if _detection_engine is None:
        _detection_engine = DetectionEngine(db)
    return _detection_engine


@router.post("/process-event")
def process_event(
    event_input: EventInput,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Process a single event through the detection engine
    
    Returns incident data if a pattern is matched, otherwise returns event processing status
    """
    try:
        # Normalize event
        processor = EventProcessor()
        normalized_event = processor.normalize_event(event_input.event, event_input.source)
        
        # Process through detection engine
        engine = get_detection_engine(db)
        incident = engine.process_event(normalized_event)
        
        if incident:
            logger.info(f"Incident created: {incident['incident_id']}")
            return {
                "status": "incident_created",
                "incident": incident,
                "event_id": normalized_event["event_id"]
            }
        else:
            return {
                "status": "processed",
                "message": "Event processed successfully, no incident created",
                "event_id": normalized_event["event_id"]
            }
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-batch")
def process_batch_events(
    batch_input: BatchEventInput,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Process multiple events in batch
    
    Can be processed in background for large batches
    """
    try:
        # Normalize events
        processor = EventProcessor()
        normalized_events = processor.normalize_batch(batch_input.events, batch_input.source)
        
        # Process through detection engine
        engine = get_detection_engine(db)
        incidents = engine.process_batch(normalized_events)
        
        logger.info(f"Processed {len(normalized_events)} events, created {len(incidents)} incidents")
        
        return {
            "status": "success",
            "events_processed": len(normalized_events),
            "incidents_created": len(incidents),
            "incidents": incidents
        }
    except Exception as e:
        logger.error(f"Error processing batch events: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_detection_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get detection engine statistics
    """
    try:
        engine = get_detection_engine(db)
        stats = engine.get_stats()
        
        return {
            "detection_stats": stats,
            "timestamp": "now"
        }
    except Exception as e:
        logger.error(f"Error getting detection stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entity/{entity_key}")
def get_entity_state(
    entity_key: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get current detection state for a specific entity (user, computer, IP)
    """
    try:
        engine = get_detection_engine(db)
        state = engine.get_entity_state(entity_key)
        
        return {
            "entity_key": entity_key,
            "state": state
        }
    except Exception as e:
        logger.error(f"Error getting entity state: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/entity/{entity_key}")
def clear_entity_state(
    entity_key: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Clear detection state for a specific entity (useful for testing or manual cleanup)
    """
    try:
        # Check user has admin role
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        
        engine = get_detection_engine(db)
        engine.clear_entity_state(entity_key)
        
        logger.info(f"Cleared entity state for: {entity_key}")
        
        return {
            "message": f"Entity state cleared for {entity_key}"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing entity state: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-event")
def create_test_event(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create test events to verify detection engine functionality
    """
    try:
        # Check user has admin role
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Create sample test events for Data Theft pattern
        test_events = [
            {
                "event": {
                    "UserName": "test.user@company.com",
                    "ComputerName": "WORKSTATION01",
                    "FileName": "sensitive_data.zip",
                    "TargetFileName": "/Users/test/Documents/sensitive_data.zip",
                    "event_simpleName": "DataStaged"
                },
                "source": "falcon"
            },
            {
                "event": {
                    "UserName": "test.user@company.com",
                    "ComputerName": "WORKSTATION01",
                    "RemoteAddressIP4": "203.0.113.45",
                    "RemotePort": 443,
                    "LocalAddressIP4": "192.168.1.100"
                },
                "source": "paloalto"
            },
            {
                "event": {
                    "UserName": "test.user@company.com",
                    "ComputerName": "WORKSTATION01",
                    "url": {"domain": "dropbox.com"}
                },
                "source": "umbrella"
            }
        ]
        
        processor = EventProcessor()
        engine = get_detection_engine(db)
        incidents = []
        
        for test_event in test_events:
            normalized = processor.normalize_event(test_event["event"], test_event["source"])
            incident = engine.process_event(normalized)
            if incident:
                incidents.append(incident)
        
        return {
            "message": "Test events created and processed",
            "events_created": len(test_events),
            "incidents_created": len(incidents),
            "incidents": incidents
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating test events: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

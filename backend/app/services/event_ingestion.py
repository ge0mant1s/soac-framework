"""
Event Ingestion Service
Handles background collection of events from devices and feeds them to the detection engine
"""
import logging
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
import os

from ..database import SessionLocal
from ..models import Device, Event, Incident
from ..connectors import get_connector
from ..detection.event_processor import EventProcessor
from ..detection.detection_engine import DetectionEngine

logger = logging.getLogger(__name__)


class EventIngestionService:
    """
    Service for ingesting events from devices
    Runs as a background task and periodically collects events
    """
    
    def __init__(self):
        self.event_processor = EventProcessor()
        self.mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
        self.collection_interval = int(os.getenv("EVENT_COLLECTION_INTERVAL", "300"))  # 5 minutes default
        self.is_running = False
        logger.info(f"Event Ingestion Service initialized (mock_mode={self.mock_mode})")
    
    async def start_background_collection(self):
        """Start background event collection task"""
        self.is_running = True
        logger.info("Starting background event collection...")
        
        while self.is_running:
            try:
                await self.collect_from_all_devices()
                await asyncio.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error in background collection: {e}", exc_info=True)
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    def stop(self):
        """Stop background event collection"""
        self.is_running = False
        logger.info("Stopping background event collection...")
    
    async def collect_from_all_devices(self):
        """Collect events from all enabled devices"""
        db = SessionLocal()
        try:
            devices = db.query(Device).filter(Device.enabled == True).all()
            
            if not devices:
                logger.debug("No enabled devices found for event collection")
                return
            
            logger.info(f"Collecting events from {len(devices)} devices")
            
            for device in devices:
                try:
                    await self.collect_from_device(device, db)
                except Exception as e:
                    logger.error(f"Error collecting from device {device.name}: {e}")
            
        finally:
            db.close()
    
    async def collect_from_device(self, device: Device, db: Session) -> Dict[str, Any]:
        """
        Collect events from a single device
        
        Args:
            device: Device model instance
            db: Database session
        
        Returns:
            Dictionary with collection results
        """
        try:
            # Get connector for device type
            connector = get_connector(
                device_type=device.type,
                config=device.config,
                mock_mode=self.mock_mode
            )
            
            # Collect events (last hour by default)
            raw_events = connector.collect_events(hours=1, limit=100)
            
            if not raw_events:
                logger.debug(f"No events collected from {device.name}")
                return {
                    "success": True,
                    "device_id": str(device.id),
                    "events_collected": 0,
                    "events_stored": 0
                }
            
            # Store events in database
            stored_count = 0
            for raw_event in raw_events:
                try:
                    # Create Event record
                    event = Event(
                        device_id=device.id,
                        timestamp=self._parse_timestamp(raw_event.get("timestamp")),
                        event_type=raw_event.get("event_type"),
                        severity=raw_event.get("severity", "info"),
                        raw_data=raw_event.get("raw_event", raw_event),
                        normalized_data=raw_event,
                        processed=False
                    )
                    
                    db.add(event)
                    stored_count += 1
                    
                except Exception as e:
                    logger.error(f"Error storing event: {e}")
            
            db.commit()
            
            # Update device statistics
            device.last_connected = datetime.utcnow()
            device.event_count += stored_count
            device.connection_status = "connected"
            
            # Update health status
            health = connector.get_health()
            device.health_status = health.get("status", "unknown")
            
            db.commit()
            
            logger.info(f"Collected {stored_count} events from {device.name}")
            
            # Process events through detection engine
            await self.process_events(device.id, db)
            
            return {
                "success": True,
                "device_id": str(device.id),
                "events_collected": len(raw_events),
                "events_stored": stored_count
            }
            
        except Exception as e:
            logger.error(f"Error in collect_from_device for {device.name}: {e}", exc_info=True)
            device.connection_status = "error"
            db.commit()
            
            return {
                "success": False,
                "device_id": str(device.id),
                "error": str(e)
            }
    
    async def process_events(self, device_id, db: Session):
        """
        Process unprocessed events through detection engine
        
        Args:
            device_id: Device UUID
            db: Database session
        """
        try:
            # Get unprocessed events
            unprocessed_events = db.query(Event).filter(
                and_(
                    Event.device_id == device_id,
                    Event.processed == False
                )
            ).limit(100).all()
            
            if not unprocessed_events:
                return
            
            logger.info(f"Processing {len(unprocessed_events)} events through detection engine")
            
            # Initialize detection engine
            detection_engine = DetectionEngine(db)
            
            for event in unprocessed_events:
                try:
                    # Process event through detection engine
                    normalized_data = event.normalized_data or {}
                    result = detection_engine.process_event(normalized_data)
                    
                    # Update event
                    event.processed = True
                    event.detection_results = result if result else None
                    
                except Exception as e:
                    logger.error(f"Error processing event {event.id}: {e}")
                    event.processed = True  # Mark as processed to avoid reprocessing
            
            db.commit()
            logger.info(f"Completed processing events for device {device_id}")
            
        except Exception as e:
            logger.error(f"Error in process_events: {e}", exc_info=True)
    
    def _parse_timestamp(self, timestamp_str: Optional[str]) -> datetime:
        """Parse timestamp string to datetime"""
        if not timestamp_str:
            return datetime.utcnow()
        
        try:
            # Try ISO format first
            if isinstance(timestamp_str, str):
                # Remove 'Z' if present
                timestamp_str = timestamp_str.rstrip('Z')
                return datetime.fromisoformat(timestamp_str)
            elif isinstance(timestamp_str, datetime):
                return timestamp_str
        except Exception:
            pass
        
        return datetime.utcnow()
    
    def manual_collect(self, device_id: str, db: Session, hours: int = 24, limit: int = 500) -> Dict[str, Any]:
        """
        Manually trigger event collection for a device
        
        Args:
            device_id: Device UUID string
            db: Database session
            hours: Hours to look back
            limit: Maximum events to collect
        
        Returns:
            Collection results dictionary
        """
        try:
            from uuid import UUID
            device = db.query(Device).filter(Device.id == UUID(device_id)).first()
            
            if not device:
                return {
                    "success": False,
                    "error": "Device not found"
                }
            
            if not device.enabled:
                return {
                    "success": False,
                    "error": "Device is disabled"
                }
            
            # Get connector
            connector = get_connector(
                device_type=device.type,
                config=device.config,
                mock_mode=self.mock_mode
            )
            
            # Collect events
            raw_events = connector.collect_events(hours=hours, limit=limit)
            
            if not raw_events:
                return {
                    "success": True,
                    "device_id": device_id,
                    "events_collected": 0,
                    "events_stored": 0,
                    "message": "No events found"
                }
            
            # Store events
            stored_count = 0
            for raw_event in raw_events:
                try:
                    event = Event(
                        device_id=device.id,
                        timestamp=self._parse_timestamp(raw_event.get("timestamp")),
                        event_type=raw_event.get("event_type"),
                        severity=raw_event.get("severity", "info"),
                        raw_data=raw_event.get("raw_event", raw_event),
                        normalized_data=raw_event,
                        processed=False
                    )
                    
                    db.add(event)
                    stored_count += 1
                    
                except Exception as e:
                    logger.error(f"Error storing event: {e}")
            
            db.commit()
            
            # Update device
            device.last_connected = datetime.utcnow()
            device.event_count += stored_count
            device.connection_status = "connected"
            
            health = connector.get_health()
            device.health_status = health.get("status", "unknown")
            
            db.commit()
            
            logger.info(f"Manual collection: {stored_count} events from {device.name}")
            
            return {
                "success": True,
                "device_id": device_id,
                "events_collected": len(raw_events),
                "events_stored": stored_count,
                "message": f"Successfully collected {stored_count} events"
            }
            
        except Exception as e:
            logger.error(f"Error in manual_collect: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_statistics(self, db: Session) -> Dict[str, Any]:
        """Get event ingestion statistics"""
        try:
            total_events = db.query(Event).count()
            processed_events = db.query(Event).filter(Event.processed == True).count()
            unprocessed_events = total_events - processed_events
            
            # Events by device
            devices = db.query(Device).all()
            device_stats = []
            
            for device in devices:
                event_count = db.query(Event).filter(Event.device_id == device.id).count()
                device_stats.append({
                    "device_id": str(device.id),
                    "device_name": device.name,
                    "device_type": device.type,
                    "event_count": event_count,
                    "last_connected": device.last_connected.isoformat() if device.last_connected else None,
                    "health_status": device.health_status
                })
            
            return {
                "total_events": total_events,
                "processed_events": processed_events,
                "unprocessed_events": unprocessed_events,
                "devices": device_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {
                "error": str(e)
            }


# Global instance
event_ingestion_service = EventIngestionService()

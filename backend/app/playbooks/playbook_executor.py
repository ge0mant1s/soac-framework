
"""
Playbook Executor - Executes automated response playbooks for incidents
"""
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from ..models import PlaybookExecution, Incident
from ..operational_models.model_loader import get_model_loader

logger = logging.getLogger(__name__)


class PlaybookExecutor:
    """
    Executes response playbooks defined in operational models
    Supports both manual and automated execution
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.model_loader = get_model_loader()
    
    def execute_playbook(
        self, 
        playbook_id: str, 
        incident_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        mode: str = "manual"
    ) -> Dict[str, Any]:
        """
        Execute a specific playbook
        
        Args:
            playbook_id: Playbook identifier (e.g., "PB_1", "PB_2")
            incident_id: Optional incident ID this playbook is responding to
            parameters: Optional parameters for playbook execution
            mode: "manual" or "automated"
        
        Returns:
            Execution result dictionary
        """
        logger.info(f"Executing playbook {playbook_id} for incident {incident_id} (mode: {mode})")
        
        # Find playbook in operational models
        playbook = self._find_playbook(playbook_id)
        if not playbook:
            raise ValueError(f"Playbook not found: {playbook_id}")
        
        # Create execution record
        execution_id = f"EXEC-{uuid.uuid4().hex[:8].upper()}"
        execution = PlaybookExecution(
            execution_id=execution_id,
            incident_id=incident_id,
            playbook_id=playbook_id,
            playbook_name=playbook.get("name", "Unknown"),
            status="running",
            steps_completed=0,
            steps_total=len(playbook.get("steps", [])),
            start_time=datetime.utcnow()
        )
        
        self.db.add(execution)
        self.db.commit()
        
        # Execute playbook steps
        try:
            results = self._execute_steps(playbook, parameters or {}, execution)
            
            # Update execution status
            execution.status = "completed"
            execution.end_time = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Playbook execution completed: {execution_id}")
            
            return {
                "execution_id": execution_id,
                "playbook_id": playbook_id,
                "playbook_name": playbook["name"],
                "status": "completed",
                "steps_completed": execution.steps_completed,
                "steps_total": execution.steps_total,
                "results": results,
                "duration_seconds": (execution.end_time - execution.start_time).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"Playbook execution failed: {str(e)}")
            execution.status = "failed"
            execution.end_time = datetime.utcnow()
            self.db.commit()
            
            return {
                "execution_id": execution_id,
                "playbook_id": playbook_id,
                "status": "failed",
                "error": str(e)
            }
    
    def execute_playbooks_for_incident(
        self, 
        incident_id: str, 
        mode: str = "automated"
    ) -> List[Dict[str, Any]]:
        """
        Execute all relevant playbooks for an incident based on decision matrix
        
        Args:
            incident_id: Incident ID
            mode: "manual" or "automated"
        
        Returns:
            List of execution results
        """
        # Get incident
        incident = self.db.query(Incident).filter_by(incident_id=incident_id).first()
        if not incident:
            raise ValueError(f"Incident not found: {incident_id}")
        
        # Get operational model
        model = self.model_loader.get_model(incident.pattern_id)
        if not model:
            logger.warning(f"Operational model not found for pattern: {incident.pattern_id}")
            return []
        
        # Determine which playbooks to execute based on decision matrix
        playbooks_to_execute = self._determine_playbooks(incident, model)
        
        # Execute playbooks
        results = []
        for playbook_id in playbooks_to_execute:
            result = self.execute_playbook(
                playbook_id=playbook_id,
                incident_id=incident_id,
                parameters={
                    "entity_key": incident.entity_key,
                    "severity": incident.severity,
                    "confidence": incident.confidence_level
                },
                mode=mode
            )
            results.append(result)
        
        return results
    
    def _find_playbook(self, playbook_id: str) -> Optional[Dict[str, Any]]:
        """Find a playbook in loaded operational models"""
        for model in self.model_loader.get_all_models().values():
            for playbook in model.get("playbooks", []):
                if playbook.get("id") == playbook_id or playbook.get("name") == playbook_id:
                    return playbook
        return None
    
    def _determine_playbooks(self, incident: Incident, model: Dict[str, Any]) -> List[str]:
        """
        Determine which playbooks to execute based on decision matrix
        
        Args:
            incident: Incident object
            model: Operational model
        
        Returns:
            List of playbook IDs to execute
        """
        decision_matrix = model.get("decision_matrix", [])
        playbooks = []
        
        # Match incident conditions against decision matrix
        for decision in decision_matrix:
            condition = decision.get("condition", "").lower()
            
            # Simple condition matching (can be enhanced)
            matched = False
            
            # Check confidence level
            if incident.confidence_level and incident.confidence_level in condition:
                matched = True
            
            # Check phase count
            phases_count = len(incident.phases_matched) if incident.phases_matched else 0
            if f"{phases_count} phase" in condition or f"≥ {phases_count}" in condition:
                matched = True
            
            # Check severity
            if incident.severity and incident.severity.lower() in condition:
                matched = True
            
            if matched:
                # Extract playbook IDs from response
                playbooks_str = decision.get("playbooks_triggered", "")
                if playbooks_str:
                    # Parse playbook references (e.g., "1-6", "1 + 2", "1, 2, 3")
                    import re
                    playbook_nums = re.findall(r'\d+', playbooks_str)
                    for num in playbook_nums:
                        playbooks.append(f"PB_{num}")
        
        # If no specific matches, execute default containment playbooks
        if not playbooks and model.get("playbooks"):
            # Execute first 2 playbooks as default (usually containment)
            playbooks = [pb["id"] for pb in model["playbooks"][:2]]
        
        return list(set(playbooks))  # Remove duplicates
    
    def _execute_steps(
        self, 
        playbook: Dict[str, Any], 
        parameters: Dict[str, Any],
        execution: PlaybookExecution
    ) -> List[Dict[str, Any]]:
        """
        Execute individual playbook steps
        
        Note: This is a simulation. In production, this would integrate with
        actual security tools (Falcon API, EntraID API, PAN-OS API, etc.)
        
        Args:
            playbook: Playbook definition
            parameters: Execution parameters
            execution: PlaybookExecution record
        
        Returns:
            List of step execution results
        """
        steps = playbook.get("steps", [])
        results = []
        
        for step in steps:
            logger.info(f"Executing step {step['step']}: {step['action']}")
            
            # Simulate step execution
            # In production, this would make actual API calls to security tools
            result = {
                "step": step["step"],
                "action": step["action"],
                "status": "completed",  # In production: "completed", "failed", "skipped"
                "output": f"Simulated execution of: {step['action']}",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Simulate different actions
            action_lower = step["action"].lower()
            
            if "isolate" in action_lower or "quarantine" in action_lower:
                result["output"] = f"Isolated endpoint: {parameters.get('entity_key', 'unknown')}"
            elif "disable" in action_lower or "revoke" in action_lower:
                result["output"] = f"Disabled account: {parameters.get('entity_key', 'unknown')}"
            elif "block" in action_lower:
                result["output"] = "Added IP/domain to blocklist"
            elif "notify" in action_lower or "alert" in action_lower:
                result["output"] = "Notification sent to SOC team"
            elif "capture" in action_lower or "collect" in action_lower:
                result["output"] = "Forensic data captured"
            
            results.append(result)
            
            # Update execution progress
            execution.steps_completed += 1
            self.db.commit()
        
        return results
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a playbook execution"""
        execution = self.db.query(PlaybookExecution).filter_by(
            execution_id=execution_id
        ).first()
        
        if not execution:
            return None
        
        return {
            "execution_id": execution.execution_id,
            "incident_id": execution.incident_id,
            "playbook_id": execution.playbook_id,
            "playbook_name": execution.playbook_name,
            "status": execution.status,
            "steps_completed": execution.steps_completed,
            "steps_total": execution.steps_total,
            "start_time": execution.start_time.isoformat() if execution.start_time else None,
            "end_time": execution.end_time.isoformat() if execution.end_time else None
        }
    
    def list_executions(
        self, 
        incident_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List playbook executions with optional filters"""
        query = self.db.query(PlaybookExecution)
        
        if incident_id:
            query = query.filter_by(incident_id=incident_id)
        if status:
            query = query.filter_by(status=status)
        
        executions = query.order_by(PlaybookExecution.created_at.desc()).all()
        
        return [
            {
                "execution_id": e.execution_id,
                "incident_id": e.incident_id,
                "playbook_id": e.playbook_id,
                "playbook_name": e.playbook_name,
                "status": e.status,
                "steps_completed": e.steps_completed,
                "steps_total": e.steps_total,
                "created_at": e.created_at.isoformat()
            }
            for e in executions
        ]

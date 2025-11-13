
"""
Operational Model API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from ..auth import get_current_user
from ..operational_models.model_loader import get_model_loader
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/operational-models", tags=["Operational Models"])


@router.get("/")
def list_operational_models(
    current_user: dict = Depends(get_current_user)
):
    """
    List all loaded operational models
    """
    try:
        model_loader = get_model_loader()
        models = model_loader.get_model_list()
        
        return {
            "models": models,
            "total": len(models)
        }
    except Exception as e:
        logger.error(f"Error listing operational models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{model_id}")
def get_operational_model(
    model_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed information about a specific operational model
    """
    try:
        model_loader = get_model_loader()
        model = model_loader.get_model(model_id)
        
        if not model:
            raise HTTPException(status_code=404, detail="Operational model not found")
        
        return model
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting operational model {model_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{model_id}/phases")
def get_model_phases(
    model_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get attack phases for a specific operational model
    """
    try:
        model_loader = get_model_loader()
        correlation_pattern = model_loader.get_correlation_pattern(model_id)
        
        if not correlation_pattern:
            raise HTTPException(status_code=404, detail="Operational model not found")
        
        return {
            "model_id": model_id,
            "pattern_id": correlation_pattern.get("pattern_id"),
            "phases": correlation_pattern.get("phases", []),
            "correlation_window": correlation_pattern.get("correlation_window"),
            "pivot_entities": correlation_pattern.get("pivot_entities", [])
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting phases for model {model_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{model_id}/playbooks")
def get_model_playbooks(
    model_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get response playbooks for a specific operational model
    """
    try:
        model_loader = get_model_loader()
        playbooks = model_loader.get_playbooks(model_id)
        
        return {
            "model_id": model_id,
            "playbooks": playbooks,
            "total": len(playbooks)
        }
    except Exception as e:
        logger.error(f"Error getting playbooks for model {model_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{model_id}/queries")
def get_model_queries(
    model_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detection queries for a specific operational model
    """
    try:
        model_loader = get_model_loader()
        queries = model_loader.get_detection_queries(model_id)
        
        return {
            "model_id": model_id,
            "queries": queries
        }
    except Exception as e:
        logger.error(f"Error getting queries for model {model_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reload")
def reload_operational_models(
    current_user: dict = Depends(get_current_user)
):
    """
    Reload all operational models from DOCX files
    """
    try:
        # Check user has admin role
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        
        model_loader = get_model_loader()
        models = model_loader.reload_models()
        
        logger.info(f"Reloaded {len(models)} operational models")
        
        return {
            "message": "Operational models reloaded successfully",
            "models_loaded": len(models),
            "model_ids": list(models.keys())
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reloading operational models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
def get_models_stats(
    current_user: dict = Depends(get_current_user)
):
    """
    Get operational models statistics
    """
    try:
        model_loader = get_model_loader()
        models = model_loader.get_all_models()
        
        total_models = len(models)
        total_playbooks = sum(len(m.get("playbooks", [])) for m in models.values())
        total_phases = sum(
            len(m.get("correlation_pattern", {}).get("phases", [])) 
            for m in models.values()
        )
        
        return {
            "total_models": total_models,
            "total_playbooks": total_playbooks,
            "total_phases": total_phases,
            "models": [
                {
                    "id": m["id"],
                    "name": m["name"],
                    "severity": m.get("alert_policy", {}).get("severity", "Unknown"),
                    "phases_count": len(m.get("correlation_pattern", {}).get("phases", [])),
                    "playbooks_count": len(m.get("playbooks", []))
                }
                for m in models.values()
            ]
        }
    except Exception as e:
        logger.error(f"Error getting models stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

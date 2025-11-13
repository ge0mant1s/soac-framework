"""
Model Loader - Loads and manages operational models from DOCX files
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from .parser import parse_operational_model

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Loads operational models from DOCX files and manages them in memory
    """
    
    def __init__(self, models_dir: str = "/home/ubuntu/Uploads"):
        self.models_dir = Path(models_dir)
        self.output_dir = Path(__file__).parent / "models"
        self.output_dir.mkdir(exist_ok=True)
        self.models: Dict[str, Dict] = {}
    
    def load_all_models(self) -> Dict[str, Dict]:
        """Load all operational model DOCX files from the models directory"""
        logger.info(f"Loading operational models from: {self.models_dir}")
        
        # Find all operational model DOCX files
        docx_files = list(self.models_dir.glob("*operational model.docx")) + \
                     list(self.models_dir.glob("*Operational Model.docx"))
        
        if not docx_files:
            logger.warning(f"No operational model files found in {self.models_dir}")
            return self.models
        
        for docx_file in docx_files:
            try:
                logger.info(f"Parsing: {docx_file.name}")
                model_data = parse_operational_model(str(docx_file), str(self.output_dir))
                self.models[model_data["id"]] = model_data
                logger.info(f"Loaded model: {model_data['name']} ({model_data['id']})")
            except Exception as e:
                logger.error(f"Failed to parse {docx_file.name}: {str(e)}")
        
        logger.info(f"Loaded {len(self.models)} operational models")
        return self.models
    
    def load_from_json(self) -> Dict[str, Dict]:
        """Load models from previously saved JSON files"""
        logger.info(f"Loading models from JSON in: {self.output_dir}")
        
        json_files = list(self.output_dir.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    model_data = json.load(f)
                    self.models[model_data["id"]] = model_data
                    logger.info(f"Loaded model from JSON: {model_data['name']}")
            except Exception as e:
                logger.error(f"Failed to load {json_file.name}: {str(e)}")
        
        return self.models
    
    def get_model(self, model_id: str) -> Optional[Dict]:
        """Get a specific model by ID"""
        return self.models.get(model_id)
    
    def get_all_models(self) -> Dict[str, Dict]:
        """Get all loaded models"""
        return self.models
    
    def get_model_list(self) -> List[Dict]:
        """Get list of models with basic info"""
        return [
            {
                "id": model["id"],
                "name": model["name"],
                "version": model["version"],
                "severity": model.get("alert_policy", {}).get("severity", "Unknown"),
                "phases_count": len(model.get("correlation_pattern", {}).get("phases", [])),
                "playbooks_count": len(model.get("playbooks", [])),
                "created_at": model.get("created_at")
            }
            for model in self.models.values()
        ]
    
    def reload_models(self) -> Dict[str, Dict]:
        """Reload all models from DOCX files"""
        self.models.clear()
        return self.load_all_models()
    
    def get_detection_queries(self, model_id: str) -> Dict:
        """Get detection queries for a specific model"""
        model = self.get_model(model_id)
        if not model:
            return {}
        return model.get("detection_queries", {})
    
    def get_playbooks(self, model_id: str) -> List[Dict]:
        """Get playbooks for a specific model"""
        model = self.get_model(model_id)
        if not model:
            return []
        return model.get("playbooks", [])
    
    def get_correlation_pattern(self, model_id: str) -> Dict:
        """Get correlation pattern for a specific model"""
        model = self.get_model(model_id)
        if not model:
            return {}
        return model.get("correlation_pattern", {})


# Global model loader instance
_model_loader: Optional[ModelLoader] = None


def get_model_loader() -> ModelLoader:
    """Get the global model loader instance"""
    global _model_loader
    if _model_loader is None:
        _model_loader = ModelLoader()
        try:
            # Try to load from JSON first (faster)
            models = _model_loader.load_from_json()
            if not models:
                # If no JSON files, parse from DOCX
                _model_loader.load_all_models()
        except Exception as e:
            logger.error(f"Error initializing model loader: {str(e)}")
    return _model_loader


"""
Configuration Processor - Process EntraID and PaloAlto NGFW rules
Converts Excel-based security rules into operational detection rules
"""

import pandas as pd
import json
import yaml
import logging
from typing import Dict, List, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigProcessor:
    """Process security configuration files from various sources"""
    
    def __init__(self, data_dir: str = 'data'):
        """
        Initialize the configuration processor
        
        Args:
            data_dir: Directory containing configuration files
        """
        self.data_dir = Path(data_dir)
        self.rules = {
            'entraid': [],
            'paloalto': [],
            'sigma': []
        }
        logger.info(f"ConfigProcessor initialized with data_dir: {data_dir}")
    
    def load_entraid_rules(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load and process EntraID authentication rules
        
        Args:
            file_path: Path to EntraID rules Excel file
            
        Returns:
            List of processed rules
        """
        try:
            df = pd.read_excel(file_path)
            logger.info(f"Loaded {len(df)} EntraID rules from {file_path}")
            
            rules = []
            for idx, row in df.iterrows():
                rule = {
                    'id': f"ENTRAID-{row.get('#', idx+1):03d}",
                    'use_case': row.get('Use Case', 'Unknown'),
                    'detection_rule': row.get('Detection Rule', ''),
                    'incident_rule': row.get('Incident Rule', ''),
                    'severity': row.get('Severity', 'Medium'),
                    'mitre_tactic': row.get('MITRE Tactic', ''),
                    'mitre_technique': row.get('MITRE Technique', ''),
                    'category': row.get('Category', ''),
                    'query': row.get('CQL Detection Query Template', ''),
                    'source': 'EntraID'
                }
                rules.append(rule)
            
            self.rules['entraid'] = rules
            return rules
            
        except Exception as e:
            logger.error(f"Error loading EntraID rules: {e}")
            return []
    
    def load_paloalto_rules(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load and process PaloAlto NGFW rules
        
        Args:
            file_path: Path to PaloAlto rules Excel file
            
        Returns:
            List of processed rules
        """
        try:
            df = pd.read_excel(file_path)
            logger.info(f"Loaded {len(df)} PaloAlto rules from {file_path}")
            
            rules = []
            for idx, row in df.iterrows():
                rule = {
                    'id': f"PALOALTO-{row.get('#', idx+1):03d}",
                    'use_case': row.get('Use Case', 'Unknown'),
                    'detection_rule': row.get('Detection Rule', ''),
                    'incident_rule': row.get('Incident Rule', ''),
                    'severity': row.get('Severity', 'Medium'),
                    'mitre_tactic': row.get('MITRE Tactic', ''),
                    'mitre_technique': row.get('MITRE Technique', ''),
                    'category': row.get('Category', ''),
                    'query': row.get('CQL Detection Query Template', ''),
                    'source': 'PaloAlto'
                }
                rules.append(rule)
            
            self.rules['paloalto'] = rules
            return rules
            
        except Exception as e:
            logger.error(f"Error loading PaloAlto rules: {e}")
            return []
    
    def export_to_json(self, output_dir: str = 'config'):
        """
        Export all loaded rules to JSON format
        
        Args:
            output_dir: Directory to save JSON files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for source, rules in self.rules.items():
            if rules:
                file_path = output_path / f"{source}_rules.json"
                with open(file_path, 'w') as f:
                    json.dump(rules, f, indent=2)
                logger.info(f"Exported {len(rules)} {source} rules to {file_path}")
    
    def export_to_yaml(self, output_dir: str = 'config'):
        """
        Export all loaded rules to YAML format (for SIGMA compatibility)
        
        Args:
            output_dir: Directory to save YAML files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for source, rules in self.rules.items():
            if rules:
                file_path = output_path / f"{source}_rules.yaml"
                with open(file_path, 'w') as f:
                    yaml.dump(rules, f, default_flow_style=False)
                logger.info(f"Exported {len(rules)} {source} rules to {file_path}")
    
    def generate_detection_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of all detection rules
        
        Returns:
            Summary dictionary with statistics
        """
        summary = {
            'total_rules': sum(len(rules) for rules in self.rules.values()),
            'by_source': {},
            'by_severity': {},
            'by_use_case': {},
            'by_mitre_tactic': {}
        }
        
        # Aggregate statistics
        all_rules = []
        for source, rules in self.rules.items():
            summary['by_source'][source] = len(rules)
            all_rules.extend(rules)
        
        # Count by severity
        for rule in all_rules:
            severity = rule.get('severity', 'Unknown')
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
        
        # Count by use case
        for rule in all_rules:
            use_case = rule.get('use_case', 'Unknown')
            summary['by_use_case'][use_case] = summary['by_use_case'].get(use_case, 0) + 1
        
        # Count by MITRE tactic
        for rule in all_rules:
            tactic = rule.get('mitre_tactic', 'Unknown')
            if tactic:
                summary['by_mitre_tactic'][tactic] = summary['by_mitre_tactic'].get(tactic, 0) + 1
        
        return summary


def main():
    """Main function for testing"""
    processor = ConfigProcessor(data_dir='data/samples')
    
    # Load rules
    entraid_rules = processor.load_entraid_rules('data/samples/entraid_rules_sample.xlsx')
    paloalto_rules = processor.load_paloalto_rules('data/samples/paloalto_rules_sample.xlsx')
    
    # Export to various formats
    processor.export_to_json(output_dir='config')
    processor.export_to_yaml(output_dir='config')
    
    # Generate summary
    summary = processor.generate_detection_summary()
    print("Detection Rules Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

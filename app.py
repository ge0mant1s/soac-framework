
#!/usr/bin/env python3
"""
SOaC Framework - Main Application
Security Operations as Code Framework for comprehensive threat detection and response
"""

import logging
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from correlation_engine import CorrelationEngine
from config_processor import ConfigProcessor
from use_case_manager import UseCaseManager
from soar_playbooks import SOARPlaybookManager
from threat_intelligence import ThreatIntelligence

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/soac_framework.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class SOaCFramework:
    """
    Main SOaC Framework application
    Orchestrates all components for security operations
    """
    
    def __init__(self, config_file: str = 'config/config_template.json'):
        """
        Initialize the SOaC Framework
        
        Args:
            config_file: Path to configuration file
        """
        logger.info("=" * 60)
        logger.info("SOaC Framework - Security Operations as Code")
        logger.info("Version: 1.0.0")
        logger.info("Organization: SOaC Framework Team")
        logger.info("=" * 60)
        
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Initialize components
        logger.info("Initializing framework components...")
        self.correlation_engine = CorrelationEngine(self.config.get('correlation', {}))
        self.config_processor = ConfigProcessor(data_dir='data')
        self.use_case_manager = UseCaseManager(self.config)
        self.soar_manager = SOARPlaybookManager(self.config.get('soar', {}))
        self.threat_intel = ThreatIntelligence(self.config)
        
        logger.info("Framework initialization complete!")
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_file}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file: {e}")
            return {}
    
    def process_configurations(self):
        """Process and load security configurations"""
        logger.info("Processing security configurations...")
        
        # Load EntraID rules
        try:
            entraid_rules = self.config_processor.load_entraid_rules(
                'data/EntraID_Authentication_Rules.xlsx'
            )
            logger.info(f"Loaded {len(entraid_rules)} EntraID rules")
        except Exception as e:
            logger.warning(f"Could not load EntraID rules: {e}")
        
        # Load PaloAlto rules
        try:
            paloalto_rules = self.config_processor.load_paloalto_rules(
                'data/PaloAlto_NGFW_Rules.xlsx'
            )
            logger.info(f"Loaded {len(paloalto_rules)} PaloAlto rules")
        except Exception as e:
            logger.warning(f"Could not load PaloAlto rules: {e}")
        
        # Export to various formats
        self.config_processor.export_to_json(output_dir='config')
        self.config_processor.export_to_yaml(output_dir='config')
        
        # Generate summary
        summary = self.config_processor.generate_detection_summary()
        logger.info(f"Detection Summary: {summary['total_rules']} total rules")
    
    def generate_reports(self):
        """Generate framework reports"""
        logger.info("Generating framework reports...")
        
        # Use case coverage report
        coverage = self.use_case_manager.get_coverage_report()
        logger.info(f"Use Case Coverage: {coverage['active_use_cases']} active, "
                   f"{coverage['unique_techniques_covered']} MITRE techniques covered")
        
        # Threat landscape summary
        threat_summary = self.threat_intel.get_threat_landscape_summary()
        logger.info(f"Threat Landscape: {threat_summary['total_threat_actors']} threat actors tracked")
        
        # Export data
        self.use_case_manager.export_use_cases('config/use_cases.json')
        self.threat_intel.export_threat_actors('config/threat_actors.json')
        
        # Create summary report
        report = {
            'framework_info': self.config.get('framework', {}),
            'use_case_coverage': coverage,
            'threat_landscape': threat_summary,
            'available_playbooks': len(self.soar_manager.list_playbooks()),
            'timestamp': Path('config/framework_report.json').write_text(
                json.dumps({
                    'framework_info': self.config.get('framework', {}),
                    'use_case_coverage': coverage,
                    'threat_landscape': threat_summary,
                    'available_playbooks': len(self.soar_manager.list_playbooks())
                }, indent=2)
            )
        }
        
        logger.info("Reports generated successfully")
    
    def run_demo(self):
        """Run a demonstration of the framework capabilities"""
        logger.info("=" * 60)
        logger.info("Running SOaC Framework Demo")
        logger.info("=" * 60)
        
        # Demo 1: List use cases
        print("\n📋 Active Use Cases:")
        for uc in self.use_case_manager.list_use_cases():
            print(f"  • {uc['title']} ({uc['severity']}) - {uc['id']}")
        
        # Demo 2: Show threat actors
        print("\n🎭 Tracked Threat Actors:")
        for actor in self.threat_intel.list_threat_actors():
            print(f"  • {actor['name']} ({actor['type']}) - Severity: {actor['severity']}")
        
        # Demo 3: List playbooks
        print("\n🔄 Available SOAR Playbooks:")
        for pb in self.soar_manager.list_playbooks():
            print(f"  • {pb['name']} - {len(pb['steps'])} steps, MTTI: {pb['mtti_target']}")
        
        # Demo 4: Simulate correlation and response
        print("\n🔍 Simulating Threat Detection and Response...")
        from datetime import datetime
        sample_events = [
            {
                'event_type': 'ProcessRollup2',
                'source': 'Falcon',
                'UserName': 'demo_user',
                'ComputerName': 'DESKTOP-DEMO',
                'CommandLine': 'powershell.exe -enc ABC123',
                'timestamp': datetime.now().isoformat()
            },
            {
                'event_type': 'NetworkConnectIP4',
                'source': 'Falcon',
                'UserName': 'demo_user',
                'ComputerName': 'DESKTOP-DEMO',
                'RemoteAddressIP4': '192.168.1.100',
                'timestamp': datetime.now().isoformat()
            },
            {
                'event_type': 'FileWriteInfo',
                'source': 'Falcon',
                'UserName': 'demo_user',
                'ComputerName': 'DESKTOP-DEMO',
                'TargetFileName': 'document.locked',
                'timestamp': datetime.now().isoformat()
            }
        ]
        
        # Correlate events
        incidents = self.correlation_engine.correlate_events(
            sample_events, 
            pattern_id='R1',
            time_window='short_term'
        )
        
        if incidents:
            incident = incidents[0]
            print(f"\n⚠️  High-Confidence Incident Detected!")
            print(f"  Incident ID: {incident['incident_id']}")
            print(f"  Pattern: {incident['pattern_id']}")
            print(f"  Confidence: {incident['confidence_level']}")
            print(f"  Phases Matched: {', '.join(incident['phases_matched'])}")
            
            # Execute playbook
            print(f"\n🚀 Executing Response Playbook...")
            result = self.soar_manager.execute_playbook('PB-R1-RANSOMWARE', incident)
            print(f"  Playbook Status: {result['status'].value}")
            print(f"  Steps Completed: {len(result['steps_completed'])}/{len(result['steps_completed']) + len(result['steps_failed'])}")
        else:
            print("  No incidents detected (threshold not met)")
        
        logger.info("=" * 60)
        logger.info("Demo Complete")
        logger.info("=" * 60)
    
    def start(self):
        """Start the framework"""
        try:
            # Process configurations
            self.process_configurations()
            
            # Generate reports
            self.generate_reports()
            
            # Run demo
            self.run_demo()
            
            logger.info("SOaC Framework is running. Press Ctrl+C to stop.")
            
        except KeyboardInterrupt:
            logger.info("Shutting down SOaC Framework...")
        except Exception as e:
            logger.error(f"Error running framework: {e}", exc_info=True)
            raise


def main():
    """Main entry point"""
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # Initialize and start framework
    framework = SOaCFramework()
    framework.start()


if __name__ == '__main__':
    main()

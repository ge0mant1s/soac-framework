
"""
Unit tests for correlation engine
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from correlation_engine import CorrelationEngine


@pytest.fixture
def correlation_engine():
    """Fixture to create a correlation engine instance"""
    config = {'confidence_threshold': 3}
    return CorrelationEngine(config)


@pytest.fixture
def sample_events():
    """Fixture to create sample events for testing"""
    return [
        {
            'event_type': 'ProcessRollup2',
            'source': 'Falcon',
            'UserName': 'test_user',
            'ComputerName': 'DESKTOP-001',
            'CommandLine': 'powershell.exe -enc ABCD',
            'timestamp': datetime.now().isoformat()
        },
        {
            'event_type': 'NetworkConnectIP4',
            'source': 'Falcon',
            'UserName': 'test_user',
            'ComputerName': 'DESKTOP-001',
            'RemoteAddressIP4': '192.168.1.100',
            'timestamp': datetime.now().isoformat()
        },
        {
            'event_type': 'FileWriteInfo',
            'source': 'Falcon',
            'UserName': 'test_user',
            'ComputerName': 'DESKTOP-001',
            'TargetFileName': 'document.encrypted',
            'timestamp': datetime.now().isoformat()
        }
    ]


def test_correlation_engine_initialization(correlation_engine):
    """Test that correlation engine initializes correctly"""
    assert correlation_engine is not None
    assert correlation_engine.confidence_threshold == 3


def test_group_by_entity(correlation_engine, sample_events):
    """Test entity grouping functionality"""
    groups = correlation_engine._group_by_entity(sample_events)
    assert len(groups) > 0


def test_correlate_events_ransomware(correlation_engine, sample_events):
    """Test ransomware pattern correlation"""
    incidents = correlation_engine.correlate_events(sample_events, pattern_id='R1')
    assert isinstance(incidents, list)
    if incidents:
        assert 'incident_id' in incidents[0]
        assert 'pattern_id' in incidents[0]


def test_confidence_calculation(correlation_engine):
    """Test confidence level calculation"""
    assert correlation_engine._calculate_confidence(4) == 'Critical'
    assert correlation_engine._calculate_confidence(3) == 'High'
    assert correlation_engine._calculate_confidence(2) == 'Medium'
    assert correlation_engine._calculate_confidence(1) == 'Low'


def test_severity_calculation(correlation_engine):
    """Test severity calculation"""
    severity = correlation_engine._calculate_severity('R1', 3)
    assert severity in ['Critical', 'High', 'Medium', 'Low']


"""
Unit tests for use case manager
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from use_case_manager import UseCaseManager, UseCaseStatus


@pytest.fixture
def use_case_manager():
    """Fixture to create a use case manager instance"""
    return UseCaseManager(config={})


def test_use_case_manager_initialization(use_case_manager):
    """Test that use case manager initializes with default use cases"""
    assert len(use_case_manager.use_cases) == 10


def test_get_use_case(use_case_manager):
    """Test getting a specific use case"""
    uc = use_case_manager.get_use_case('UC-001-RANSOMWARE')
    assert uc is not None
    assert uc['title'] == 'Ransomware Detection and Response'


def test_list_use_cases(use_case_manager):
    """Test listing all use cases"""
    all_use_cases = use_case_manager.list_use_cases()
    assert len(all_use_cases) == 10


def test_list_active_use_cases(use_case_manager):
    """Test listing active use cases"""
    active = use_case_manager.list_use_cases(status=UseCaseStatus.ACTIVE)
    assert len(active) > 0


def test_update_use_case_status(use_case_manager):
    """Test updating use case status"""
    use_case_manager.update_use_case_status('UC-001-RANSOMWARE', UseCaseStatus.TUNING)
    uc = use_case_manager.get_use_case('UC-001-RANSOMWARE')
    assert uc['status'] == UseCaseStatus.TUNING


def test_coverage_report(use_case_manager):
    """Test generating coverage report"""
    report = use_case_manager.get_coverage_report()
    assert 'total_use_cases' in report
    assert 'active_use_cases' in report
    assert 'unique_techniques_covered' in report
    assert report['total_use_cases'] == 10

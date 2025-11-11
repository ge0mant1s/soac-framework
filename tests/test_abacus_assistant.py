import pytest
from unittest.mock import patch
from ai_engine.abacus_assistant import AbacusAIAssistant

@pytest.fixture(autouse=True)
def set_abacus_api_key_env(monkeypatch):
    monkeypatch.setenv("ABACUS_API_KEY", "fake_api_key")

@pytest.fixture
def abacus_assistant():
    return AbacusAIAssistant(api_key="fake_key")

@patch('ai_engine.abacus_assistant.requests.post')
def test_natural_language_to_cql(mock_post, abacus_assistant):
    mock_post.return_value.json.return_value = {"text": "event.outcome = failure"}
    mock_post.return_value.raise_for_status = lambda: None

    result = abacus_assistant.natural_language_to_cql("failed login attempts")
    assert "event.outcome" in result["cql"]

@patch('ai_engine.abacus_assistant.requests.post')
def test_summarize_incident(mock_post, abacus_assistant):
    mock_post.return_value.json.return_value = {"text": "Summary text"}
    mock_post.return_value.raise_for_status = lambda: None

    summary = abacus_assistant.summarize_incident("Some incident details")
    assert summary == "Summary text"
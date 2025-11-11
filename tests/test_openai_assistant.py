import pytest
from unittest.mock import patch, MagicMock
from ai_engine.openai_assistant import OpenAIAssistant

@pytest.fixture(autouse=True)
def set_openai_api_key_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake_api_key")

@pytest.fixture
def openai_assistant():
    return OpenAIAssistant()

def test_natural_language_to_cql(openai_assistant):
    with patch.object(openai_assistant.client.chat.completions, 'create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="event.outcome = failure"))]
        mock_create.return_value = mock_response

        result = openai_assistant.natural_language_to_cql("failed login attempts")
        assert "event.outcome" in result["cql"]

def test_summarize_incident(openai_assistant):
    with patch.object(openai_assistant.client.chat.completions, 'create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Summary text"))]
        mock_create.return_value = mock_response

        summary = openai_assistant.summarize_incident("Some incident details")
        assert summary == "Summary text"
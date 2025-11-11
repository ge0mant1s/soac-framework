import pytest
from unittest.mock import patch, MagicMock
from ai_engine.ai_assistant import AIAssistant

@pytest.fixture(autouse=True)
def set_openai_api_key_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake_api_key")

@pytest.fixture
def ai():
    return AIAssistant()

def test_nl_to_cql_mock(ai):
    with patch.object(ai.client.chat.completions, 'create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="mock cql"))]
        mock_create.return_value = mock_response

        result = ai.natural_language_to_cql("test query")
        assert "mock cql" in result["cql"]

def test_summarize_incident_mock(ai):
    with patch.object(ai.client.chat.completions, 'create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="mock summary"))]
        mock_create.return_value = mock_response

        summary = ai.summarize_incident("incident text")
        assert "mock summary" == summary
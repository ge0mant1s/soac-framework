import pytest
from ai_engine.factory import get_ai_assistant
from ai_engine.openai_assistant import OpenAIAssistant
from ai_engine.abacus_assistant import AbacusAIAssistant

@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake_api_key")
    monkeypatch.setenv("ABACUS_API_KEY", "fake_api_key")

def test_get_ai_assistant_openai():
    ai = get_ai_assistant("openai")
    assert isinstance(ai, OpenAIAssistant)

def test_get_ai_assistant_abacus():
    ai = get_ai_assistant("abacus")
    assert isinstance(ai, AbacusAIAssistant)

def test_get_ai_assistant_invalid():
    with pytest.raises(ValueError):
        get_ai_assistant("unknown")
from .openai_assistant import OpenAIAssistant
from .abacus_assistant import AbacusAIAssistant

def get_ai_assistant(provider: str = "abacus", **kwargs):
    if provider.lower() == "openai":
        return OpenAIAssistant(**kwargs)
    elif provider.lower() == "abacus":
        return AbacusAIAssistant(**kwargs)
    else:
        raise ValueError(f"Unknown AI provider: {provider}")
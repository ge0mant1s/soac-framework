from abc import ABC, abstractmethod

class BaseAIAssistant(ABC):
    @abstractmethod
    def natural_language_to_cql(self, nl_query: str) -> dict:
        pass

    @abstractmethod
    def summarize_incident(self, incident_text: str) -> str:
        pass
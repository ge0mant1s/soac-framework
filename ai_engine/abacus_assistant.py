"""
SOaC Abacus Engine
"""

import os
import requests
from .base_ai import BaseAIAssistant

class AbacusAIAssistant(BaseAIAssistant):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ABACUS_API_KEY")
        if not self.api_key:
            raise ValueError("ABACUS_API_KEY environment variable not set")
        self.endpoint = "https://api.abacus.ai/v1/llm"  # Replace with actual Abacus endpoint

    def natural_language_to_cql(self, nl_query: str) -> dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "prompt": f"Convert this natural language query to a CQL query:\n\n{nl_query}\n\nCQL:",
            "max_tokens": 150,
            "temperature": 0
        }
        response = requests.post(f"{self.endpoint}/completions", json=data, headers=headers)
        response.raise_for_status()
        cql = response.json().get("text", "").strip()
        return {
            "cql": cql,
            "platform": "generic",
            "confidence": 0.95,
            "description": "Abacus AI-generated CQL query"
        }

    def summarize_incident(self, incident_text: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "prompt": f"Summarize this security incident in a concise way:\n\n{incident_text}",
            "max_tokens": 100,
            "temperature": 0.5
        }
        response = requests.post(f"{self.endpoint}/completions", json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("text", "").strip()
"""
SOaC OpenAI Engine
"""

import os
import openai
from .base_ai import BaseAIAssistant

class OpenAIAssistant(BaseAIAssistant):
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = openai.OpenAI()

    def natural_language_to_cql(self, nl_query: str) -> dict:
        prompt = f"Convert this natural language query to a CQL query:\n\n{nl_query}\n\nCQL:"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0
        )
        cql = response.choices[0].message.content.strip()
        return {
            "cql": cql,
            "platform": "generic",
            "confidence": 0.95,
            "description": "OpenAI-generated CQL query"
        }

    def summarize_incident(self, incident_text: str) -> str:
        prompt = f"Summarize this security incident in a concise way:\n\n{incident_text}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
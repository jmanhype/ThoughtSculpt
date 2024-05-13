# llm_integrations/anthropic_client.py
import anthropic

class AnthropicClient:
    def __init__(self, api_key):
        self.client = anthropic.Client(api_key)

    def generate_text(self, messages, model="claude-3-opus-20240229", max_tokens=1024):
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages
        }
    def generate_text(self, prompt, max_tokens=100, temperature=0.7):
        response = self.client.complete(
            prompt=prompt,
            max_tokens_to_sample=max_tokens,
            temperature=temperature,
        )
        return response.completion
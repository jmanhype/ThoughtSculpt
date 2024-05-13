# llm_integrations/groq_client.py
import os
import requests

class GroqClient:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.api_base = "https://api.groq.com"

    def generate_text(self, messages, model="llama3-8b-8192", stream=False):
        url = f"{self.api_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "messages": messages,
            "model": model,
        }
        response = requests.post(url, headers=headers, json=data, stream=stream)
        if stream:
            for line in response.iter_lines():
                if line:
                    yield json.loads(line.decode('utf-8'))
        else:
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

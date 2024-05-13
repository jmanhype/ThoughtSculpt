import openai
from thoughtsculpt.config import settings  # Import settings module
import requests
import json

class OpenAIClient:
    def __init__(self):
        openai.api_key = settings.openai_api_key  # Use API key from settings
        self.api_base = settings.openai_api_base  # Use API base from settings

    def generate_text(self, prompt=None, messages=None, num_completions=1, max_tokens=100, model="text-davinci-002", temperature=0.7, frequency_penalty=0, organization_id=None, project_id=None, stream=False):
        headers = {
            "Authorization": f"Bearer {openai.api_key}",
            "Content-Type": "application/json"
        }
        if organization_id:
            headers["OpenAI-Organization"] = organization_id
        if project_id:
            headers["OpenAI-Project"] = project_id
        data = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "n": num_completions,
            "frequency_penalty": frequency_penalty,
            "stream": stream
        }
        if messages:
            data["messages"] = messages
        else:
            data["prompt"] = prompt

        response = requests.post(f"{self.api_base}/chat/completions", headers=headers, json=data, stream=stream)
        if stream:
            for line in response.iter_lines():
                if line:
                    yield json.loads(line.decode('utf-8'))
        else:
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

    def upload_file(self, file_path, purpose):
        headers = {
            "Authorization": f"Bearer {openai.api_key}",
            "Content-Type": "multipart/form-data"
        }
        files = {'file': open(file_path, 'rb')}
        data = {'purpose': purpose}
        response = requests.post(f"{self.api_base}/files", headers=headers, files=files, data=data)
        response.raise_for_status()
        return response.json()

    def list_files(self, purpose=None):
        headers = {"Authorization": f"Bearer {openai.api_key}"}
        params = {'purpose': purpose} if purpose else {}
        response = requests.get(f"{self.api_base}/files", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def retrieve_file(self, file_id):
        headers = {"Authorization": f"Bearer {openai.api_key}"}
        response = requests.get(f"{self.api_base}/files/{file_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    def delete_file(self, file_id):
        headers = {"Authorization": f"Bearer {openai.api_key}"}
        response = requests.delete(f"{self.api_base}/files/{file_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    def retrieve_file_content(self, file_id):
        headers = {"Authorization": f"Bearer {openai.api_key}"}
        response = requests.get(f"{self.api_base}/files/{file_id}/content", headers=headers)
        response.raise_for_status()
        return response.content

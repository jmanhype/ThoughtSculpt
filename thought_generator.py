from thoughtsculpt.llm_integration.openai_client import OpenAIClient

class ThoughtGenerator:
    def __init__(self, api_key):
        self.client = OpenAIClient(api_key)

    def generate(self, solution, feedback_text, task_description):
        prompt = f"{task_description}\n\nCurrent solution: {solution}\n\nFeedback: {feedback_text}\n\nCan you provide a revised solution?"
        response = self.client.generate_text(prompt, num_completions=3)
        candidate_solutions = [candidate.strip() for candidate in response.split("\n")]
        return candidate_solutions
from thoughtsculpt.llm_integration.openai_client import OpenAIClient

class ThoughtEvaluator:
    def __init__(self, api_key):
        self.client = OpenAIClient(api_key)

    def evaluate(self, solution, task_description):
        prompt = f"{task_description}\n\nCurrent solution: {solution}\n\nCan you evaluate the current solution and provide some feedback?"
        response = self.client.generate_text(prompt)
        feedback_text = response.strip()
        feedback_score = self.get_feedback_score(feedback_text)
        return feedback_text, feedback_score

    def get_feedback_score(self, feedback_text):
        # Implement logic to extract numerical feedback score from the feedback text
        # You can use sentiment analysis or other techniques here
        pass
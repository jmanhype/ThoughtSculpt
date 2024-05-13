# tests/test_thought_evaluator.py
import pytest
from unittest.mock import MagicMock
from thoughtsculpt.thought_evaluator import ThoughtEvaluator

@pytest.fixture
def mock_openai_client():
    client = MagicMock()
    client.generate_text.return_value = ["Great solution, but consider adding more examples."]
    return client

@pytest.fixture
def thought_evaluator(mock_openai_client):
    evaluator = ThoughtEvaluator(api_key="fake_api_key")
    evaluator.client = mock_openai_client
    return evaluator

def test_evaluate(thought_evaluator):
    solution = "Implement unit tests for all modules."
    task_description = "Ensure code reliability."
    feedback_text, feedback_score = thought_evaluator.evaluate(solution, task_description)
    assert feedback_text == "Great solution, but consider adding more examples."
    assert feedback_score is not None  # Assuming get_feedback_score is implemented

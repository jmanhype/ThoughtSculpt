# tests/test_thought_generator.py
import pytest
from unittest.mock import MagicMock
from thoughtsculpt.thought_generator import ThoughtGenerator

@pytest.fixture
def mock_openai_client():
    client = MagicMock()
    client.generate_text.return_value = ["Solution 1", "Solution 2", "Solution 3"]
    return client

@pytest.fixture
def thought_generator(mock_openai_client):
    generator = ThoughtGenerator(api_key="fake_api_key")
    generator.client = mock_openai_client
    return generator

def test_generate(thought_generator):
    solution = "Refactor the codebase."
    feedback_text = "Looks good, but improve readability."
    task_description = "Improve code quality."
    candidate_solutions = thought_generator.generate(solution, feedback_text, task_description)
    assert len(candidate_solutions) == 3
    assert "Solution 1" in candidate_solutions
    pass
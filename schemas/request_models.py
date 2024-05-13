from pydantic import BaseModel

class ThoughtSculptRequest(BaseModel):
    task_description: str
    initial_solution: str
    max_depth: int
    num_simulations: int

class EvaluationRequest(BaseModel):
    solution: str
    task_description: str

class GenerationRequest(BaseModel):
    solution: str
    feedback_text: str
    task_description: str
    
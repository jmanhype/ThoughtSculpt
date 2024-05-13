from pydantic import BaseModel

class ThoughtSculptInput(BaseModel):
    task_description: str
    initial_solution: str
    max_depth: int
    num_simulations: int

class ThoughtSculptOutput(BaseModel):
    final_solution: str

class EvaluationInput(BaseModel):
    solution: str
    task_description: str

class EvaluationOutput(BaseModel):
    feedback_text: str
    feedback_score: float

class GenerationInput(BaseModel):
    solution: str
    feedback_text: str
    task_description: str

class GenerationOutput(BaseModel):
    candidate_solutions: list[str]
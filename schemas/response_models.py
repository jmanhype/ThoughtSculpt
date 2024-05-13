from pydantic import BaseModel

class ThoughtSculptResponse(BaseModel):
    final_solution: str

class EvaluationResponse(BaseModel):
    feedback_text: str
    feedback_score: float

class GenerationResponse(BaseModel):
    candidate_solutions: list[str]
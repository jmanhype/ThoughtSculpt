from fastapi import APIRouter, Depends, HTTPException
from thoughtsculpt.schemas.request_models import ThoughtSculptRequest, EvaluationRequest, GenerationRequest
from thoughtsculpt.schemas.response_models import ThoughtSculptResponse, EvaluationResponse, GenerationResponse
from thoughtsculpt.services.thought_process import ThoughtProcess
from thoughtsculpt.utils.logger import get_logger
from thoughtsculpt.data.models import Task, get_session

router = APIRouter()

logger = get_logger(__name__)

@router.post("/thoughtsculpt", response_model=ThoughtSculptResponse)
def thoughtsculpt(request: ThoughtSculptRequest):
    logger.info(f"Received request: {request}")
    try:
        session = get_session()
        new_task = Task(description=request.task_description, solution=request.initial_solution)
        session.add(new_task)
        session.commit()

        thought_process = ThoughtProcess(request.task_description, request.initial_solution, api_key)
        final_solution = thought_process.sculpt_thought(request.max_depth, request.num_simulations)
        return ThoughtSculptResponse(final_solution=final_solution)
    except Exception as e:
        session.rollback()
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/update_solution", response_model=ThoughtSculptResponse)
def update_solution(task_id: int, new_solution: str):
    session = get_session()
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        task.solution = new_solution
        session.commit()
        return {"message": "Solution updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest):
    try:
        thought_evaluator = ThoughtEvaluator(api_key)
        feedback_text, feedback_score = thought_evaluator.evaluate(request.solution, request.task_description)
        return EvaluationResponse(feedback_text=feedback_text, feedback_score=feedback_score)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate", response_model=GenerationResponse)
def generate(request: GenerationRequest):
    try:
        thought_generator = ThoughtGenerator(api_key)
        candidate_solutions = thought_generator.generate(request.solution, request.feedback_text, request.task_description)
        return GenerationResponse(candidate_solutions=candidate_solutions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return GenerationResponse(candidate_solutions=candidate_solutions)

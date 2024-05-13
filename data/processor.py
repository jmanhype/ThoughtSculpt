# data/processor.py
def preprocess_task_description(task_description):
    # Perform any necessary preprocessing on the task description
    processed_description = task_description.strip().lower()
    return processed_description

def postprocess_solution(solution):
    # Perform any necessary postprocessing on the generated solution
    processed_solution = solution.strip().capitalize()
    return processed_solution
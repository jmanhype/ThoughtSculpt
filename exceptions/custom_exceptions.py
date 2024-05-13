# exceptions/custom_exceptions.py
class ThoughtSculptError(Exception):
    """Base class for ThoughtSculpt exceptions."""
    pass

class InvalidTaskDescriptionError(ThoughtSculptError):
    """Exception raised when the task description is invalid."""
    pass

class InvalidSolutionError(ThoughtSculptError):
    """Exception raised when the solution is invalid."""
    pass

class APIClientError(ThoughtSculptError):
    """Exception raised when an error occurs with the API client."""
    pass
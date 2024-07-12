class NoActiveTasksError(Exception):
    """Exception raised when queryset for tasks is empty."""
    def __init__(self, message: str = 'No tasks found in database.') -> None:
        self.message = message
        super().__init__(self.message)


class NoTaskValueProvidedError(Exception):
    """Exception raised when one of values needed for saving a Task is missing."""
    def __init__(self, message: str = 'No required value provided.') -> None:
        self.message = message
        super().__init__(self.message)

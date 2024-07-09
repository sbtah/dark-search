class NoActiveTasksError(Exception):
    """Exception raised when queryset for tasks is empty."""
    def __init__(self, message='No tasks found in database.'):
        self.message = message
        super().__init__(self.message)


class NoTaskValueProvidedError(Exception):
    """Exception raised when one of values needed for saving a Task is missing."""
    def __init__(self, message='No required value provided.'):
        self.message = message
        super().__init__(self.message)

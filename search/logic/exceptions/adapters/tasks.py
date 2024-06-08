class NoTasksError(Exception):
    """Exception raised when queryset for tasks is empty."""
    def __init__(self, message="No tasks found in database."):
        self.message = message
        super().__init__(self.message)
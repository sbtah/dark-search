class NoUserAgentsError(Exception):
    """Exception raised when queryset of agents is empty."""
    def __init__(self, message="No user agents found in database."):
        self.message = message
        super().__init__(self.message)
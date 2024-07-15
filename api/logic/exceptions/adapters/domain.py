class NoDomainValueProvidedError(Exception):
    """Exception raised when one of the values needed for saving a Domain is missing."""
    def __init__(self, message: str = 'No required value provided.') -> None:
        self.message = message
        super().__init__(self.message)

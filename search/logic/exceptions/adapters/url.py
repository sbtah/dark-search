class WrongTypeProvidedError(Exception):
    """Exception raised while validating types on creation of Url objects."""
    def __init__(self, message="Wrong type given for value"):
        self.message = message
        super().__init__(self.message)

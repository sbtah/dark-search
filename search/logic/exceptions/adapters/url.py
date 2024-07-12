class WrongTypeProvidedError(Exception):
    """Exception raised while validating types on creation of Url objects."""
    def __init__(self, message: str = 'Wrong type provided for Url attribute.') -> None:
        self.message = message
        super().__init__(self.message)


class WrongValueProvidedError(Exception):
    """Exception raised while validating values on creation of Url objects."""
    def __init__(self, message: str = 'Wrong value provided for Url attribute.') -> None:
        self.message = message
        super().__init__(self.message)

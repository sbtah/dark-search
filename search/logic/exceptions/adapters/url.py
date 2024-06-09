class WrongTypeProvidedError(Exception):
    """Exception raised while validating types on creation of Url objects."""
    def __init__(self, message='Wrong type provided for Url attribute.'):
        self.message = message
        super().__init__(self.message)

class WrongValueProvidedError(Exception):
    """Exception raised while validating values on creation of Url objects."""
    def __init__(self, message='Wrong value provided for Url attribute.'):
        self.message = message
        super().__init__(self.message)
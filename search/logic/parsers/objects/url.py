class Url:
    """Hashable object representing url."""

    def __init__(self, value: str, anchor: str='', number_of_requests: int=0):
        self.value: str = value
        self.anchor: str = anchor
        self.number_of_requests: int = number_of_requests

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __hash__(self):
        return hash(str(self.value))

    def __eq__(self, other):
        return self.value == other.value

    def serialize(self):
        return self.__dict__

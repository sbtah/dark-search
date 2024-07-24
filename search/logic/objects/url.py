class Url:
    """Hashable object representing url."""

    def __init__(self, value: str, anchor: str = '', number_of_requests: int = 0) -> None:
        self.value: str = value
        self.anchor: str = anchor
        self.number_of_requests: int = number_of_requests

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(str(self.value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Url):
            return NotImplemented
        return self.value == other.value

    def serialize(self) -> dict:
        return self.__dict__

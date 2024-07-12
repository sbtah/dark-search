from utilities.logging import logger


class BaseAdapter:
    """Base class for all Adapters."""

    def __init__(self) -> None:
        self.logger = logger

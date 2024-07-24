from utilities.log import logger


class BaseProcessor:
    """Base class for all Processors."""

    def __init__(self) -> None:
        self.logger = logger

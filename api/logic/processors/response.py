from logic.processors.base import BaseProcessor


class ResponseProcessor(BaseProcessor):
    """
    Crawler's response processor.
    Here data received from crawler is parsed
    and new objects are created or updated.
    """

    def parse(self):
        ...

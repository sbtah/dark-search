from base64 import b64encode


class Converter:
    """
    Helper tool designed to convert bytes response to base64 string.
    Created for converting favicons for tracking.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def convert(bytes_content: bytes) -> str:
        """Convert bytes response to base64 string."""
        b64_string = b64encode(bytes_content).decode("utf-8")
        return b64_string
from base64 import b64encode
from utilities.log import logger


class Converter:
    """
    Helper tool designed to convert bytes response to base64 string.
    Created for converting favicons for tracking.
    """

    def __init__(self) -> None:
        self.logger = logger

    def convert_bytes_to_base64(self, bytes_content: bytes) -> str | None:
        """Convert bytes from response object to base64 string."""
        try:
            b64_string: str = b64encode(bytes_content).decode('utf-8')
            return b64_string
        except Exception as exc:
            self.logger.error(
                f'({Converter.convert_bytes_to_base64.__qualname__}): exception="{exc.__class__}", '
                f'message="{exc}"', exc_info=True,
            )
            return None

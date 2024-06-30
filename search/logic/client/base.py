from utilities.logging import logger
from logging import Logger
from django.conf import settings
from logic.adapters.url import UrlAdapter


class BaseClient:
    """
    Base class for Api client.
    """

    def __init__(self) -> None:
        self.logger: Logger = logger
        self.url_adapter: UrlAdapter = UrlAdapter()
        self.base_url: str = settings.API_BASE_URL
        self.api_key: str = settings.API_KEY
        self.post_response_url: str = f'{self.base_url}{settings.API_POST_RESPONSE_ENDPOINT}'
        self.post_summary_url: str = f'{self.base_url}{settings.API_POST_SUMMARY_ENDPOINT}'
    

    def prepare_auth_headers(self) -> dict:
        """Prepare authorization headers for next request."""
        return {
            'Authorization': f'Token {self.api_key}',
        }

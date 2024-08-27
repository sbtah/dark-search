from logging import Logger

from django.conf import settings
from logic.adapters.url import UrlAdapter
from logic.objects.url import Url
from utilities.log import logger


class BaseApiClient:
    """
    Base class for the Api client.
    """

    def __init__(self) -> None:
        self.logger: Logger = logger
        self.url_adapter: UrlAdapter = UrlAdapter()
        self.max_retries: int = 3
        self.base_url: str = settings.API_BASE_URL
        self.api_key: str = settings.API_KEY
        self.post_response_url: Url = self.url_adapter.create_url_object(
            f'{self.base_url}{settings.API_POST_RESPONSE_ENDPOINT}'
        )
        self.post_summary_url: Url = self.url_adapter.create_url_object(
            f'{self.base_url}{settings.API_POST_SUMMARY_ENDPOINT}'
        )

    def prepare_headers(self) -> dict:
        """Prepare authorization headers for the next request."""
        return {
            'Authorization': f'Token {self.api_key}',
        }

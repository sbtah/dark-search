from utilities.logging import logger
from django.conf import settings


class BaseClient:
    """
    Base class for Api client.
    """

    def __init__(self):
        self.logger = logger
        self.base_url = settings.API_BASE_URL
        self.api_key = settings.API_KEY
        self.post_response_url = f'{self.base_url}{settings.API_POST_RESPONSE_URL}'
        self.post_summary_url = f'{self.base_url}{settings.API_POST_SUMMARY_URL}'

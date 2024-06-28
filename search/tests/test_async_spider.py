"""
Test cases for AsyncSpider class.
"""
from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from httpx import HTTPError, Response
from logic.spiders.asynchronous import AsyncSpider


@pytest.fixture
def spider(example_url_object):
    """Fixture returning an instance of AsyncSpider class."""
    spider = AsyncSpider(
        initial_url=example_url_object,
        proxy='http://test:8118',
        user_agent='Mozilla/Test',
    )
    return spider

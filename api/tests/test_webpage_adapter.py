"""
Test cases for Webpage Adapter class.
"""
from unittest.mock import MagicMock

import pytest
from crawled.models.webpage import Data, Webpage
from logic.adapters.webpage import WebpageAdapter


pytestmark = pytest.mark.django_db


@pytest.fixture
def adapter() -> WebpageAdapter:
    """
    Fixture returning instance of WebpageAdapter.
    Logging is turned off in testing.
    """
    adapter: WebpageAdapter = WebpageAdapter()
    adapter.logger = MagicMock()
    return adapter


class TestWebpageAdapter:
    """Test cases for WebpageAdapter functionality."""

    def test_webpage_adapter_get_or_create_webpage_by_url_return_existing_webpage(
        self,
        adapter,
        example_webpage,
    ) -> None:
        """
        Test that get_or_create_webpage_by_url is successfully returning an existing Webpage object.
        """
        return_value = adapter.get_or_create_webpage_by_url(url='http://test.com')
        assert isinstance(return_value, Webpage)
        assert return_value.url == 'http://test.com'

    def test_webpage_adapter_get_or_create_webpage_by_url_create_new_object(
        self,
        adapter,
        example_domain,
    ) -> None:
        """
        Test that get_or_create_webpage_by_url is successfully creating a new Webpage object.
        """
        return_value = adapter.get_or_create_webpage_by_url(domain=example_domain, url='http://test.com')
        assert isinstance(return_value, Webpage)
        assert return_value.url == 'http://test.com'
        assert return_value.parent_domain == example_domain

    def test_webpage_adapter_get_or_create_webpage_by_url_raises_exception_if_no_domain(
        self,
        adapter,
    ) -> None:
        """
        Test that get_or_create_webpage_by_url is successfully raising AssertError if no domain provided.
        """
        with pytest.raises(AssertionError):
            adapter.get_or_create_webpage_by_url(url='http://test.com')

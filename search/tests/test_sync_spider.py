"""
Test cases for SyncSpider class.
"""
from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from httpx import HTTPError, Response
from logic.spiders.synchronous import SyncSpider


@pytest.fixture
def spider(example_url_object):
    """Fixture returning an instance of SyncSpider class."""
    spider = SyncSpider(
        initial_url=example_url_object,
        proxy='http://test:8118',
        user_agent='Mozilla/Test',
    )
    spider.logger = MagicMock()
    return spider


class TestSyncSpider:
    """Test cases for SyncSpider functionality."""

    @patch('logic.spiders.synchronous.httpx.Client.get')
    def test_sync_spider_get_method_returns_response_and_url_object(
        self,
        mock_get,
        spider,
        example_text_response,
        example_url_object,
    ):
        """Test that SyncSpider get method is returning tuple with Response object and Url object."""
        mock_response = MagicMock(spec=Response, status_code=200)
        mock_get.return_value = (mock_response, example_url_object)

        response = spider.get(url=spider.initial_url)
        mock_get.assert_called_once()
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[1].number_of_requests == 1

    @patch('logic.spiders.synchronous.httpx.Client.get')
    def test_sync_spider_get_method_returns_none_on_exception(
        self, mock_get, spider, example_url_object
    ):
        """Test that SyncSpider get method is returning tuple with None and Url object on exception."""
        mock_get.side_effect = HTTPError('Error!')

        response = spider.get(url=spider.initial_url)
        mock_get.assert_called_once()
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[1].number_of_requests == 1
        assert response[0] is None

    @patch('logic.spiders.synchronous.SyncSpider.get')
    def test_sync_spider_request_method_returns_proper_response(
        self, mock_get, spider, example_text_response, example_url_object
    ):
        """
        Test that SyncSpider request method is returning desired response dictionary.
        """
        mock_response = MagicMock(spec=Response, status_code=200)
        mock_response.text = example_text_response
        mock_response.url = example_url_object.value
        mock_response.headers = {'server': 'test_server'}
        mock_response.elapsed = timedelta(seconds=10)
        mock_get.return_value = mock_response, example_url_object

        response = spider.request()
        mock_get.assert_called_once()

        assert isinstance(response, dict)
        assert {
            'requested_url',
            'status',
            'responded_url',
            'server',
            'content_type',
            'response_time',
            'visited',
            'text',
            'page_title',
            'meta_title',
            'meta_description',
            'on_page_urls',
            'processed_urls',
            'favicon_url'
        } == set(response.keys())

    @patch('logic.spiders.synchronous.SyncSpider.get')
    def test_sync_spider_request_method_returns_desired_data_for_wrong_status_codes(
        self, mock_get, spider, example_url_object,
    ):
        """
        Test that SyncSpider request method is returning desired response
            when status codes are not in 200 or 300 range.
        """
        mock_response = MagicMock(spec=Response, status_code=404)
        mock_response.text = ''
        mock_response.url = example_url_object.value
        mock_response.elapsed = timedelta(10)
        mock_response.headers = {'server': 'test_server'}
        mock_get.return_value = mock_response, example_url_object
        response = spider.request()
        mock_get.assert_called_once()

        assert isinstance(response, dict)
        assert {
            'requested_url',
            'status',
            'responded_url',
            'server',
            'content_type',
            'response_time',
            'visited',
        } == set(response.keys())

    @patch('logic.spiders.synchronous.SyncSpider.get')
    def test_sync_spider_request_method_returns_desired_data_for_none_response(
        self, mock_get, spider, example_url_object,
    ):
        """
        Test that SyncSpider request method is returning desired response when response is None.
        """
        mock_get.return_value = None, example_url_object
        response = spider.request()
        mock_get.assert_called_once()

        assert isinstance(response, dict)
        assert {'requested_url', 'status'} == set(response.keys())
        assert response['status'] is None

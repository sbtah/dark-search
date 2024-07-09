"""
Test cases for AsyncSpider class.
"""
from datetime import timedelta
from unittest.mock import MagicMock, patch, call

import pytest
from httpx import HTTPError, Response
from logic.spiders.asynchronous import AsyncSpider
from logic.parsers.objects.url import Url


@pytest.fixture
def spider(example_url_object):
    """Fixture returning an instance of AsyncSpider class."""
    spider = AsyncSpider(
        initial_url=example_url_object,
        proxy='http://test:8118',
        user_agent='Mozilla/Test',
        max_requests=5,
        sleep_time=1,
    )
    return spider


class TestAsyncSpider:
    """Test cases for AsyncSpider class."""

    @pytest.mark.asyncio
    @patch('logic.spiders.asynchronous.httpx.AsyncClient.get')
    async def test_async_spider_get_method_returns_response_and_url_object(
        self,
        mock_get,
        spider,
        example_text_response,
        example_url_object,
    ):
        """
        Test that AsyncSpider get method is returning tuple with Response and Url object.
        """
        mock_response = MagicMock(spec=Response, status_code=200)
        mock_get.return_value = mock_response, example_url_object

        response = await spider.get(url=spider.initial_url)
        mock_get.assert_called_once()
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[1].number_of_requests == 1

    @pytest.mark.asyncio
    @patch('logic.spiders.asynchronous.httpx.AsyncClient.get')
    async def test_async_spider_get_method_returns_none_on_exception(
        self, mock_get, spider, example_url_object,
    ):
        """
        Test that AsyncSpider get method is returning tuple with None and Url object on exception.
        """
        mock_get.side_effect = HTTPError('Error!')

        response = await spider.get(url=spider.initial_url)
        mock_get.assert_called_once()
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[1].number_of_requests == 1
        assert response[0] is None

    @pytest.mark.asyncio
    @patch('logic.spiders.asynchronous.AsyncSpider.get')
    async def test_async_spider_request_method_returns_proper_response(
        self, mock_get, spider, example_text_response, example_url_object
    ):
        """
        Test that AsyncSpider request method is returning desired response dictionary.
        """
        mock_response = MagicMock(spec=Response, status_code=200)
        mock_response.text = example_text_response
        mock_response.url = example_url_object.value
        mock_response.headers = {'server': 'test_server'}
        mock_response.elapsed = timedelta(seconds=10)
        mock_get.return_value = mock_response, example_url_object

        response = await spider.request(spider.initial_url)
        mock_get.assert_called_once()

        assert isinstance(response, dict)
        assert {
            'requested_url',
            'responded_url',
            'status',
            'server',
            'elapsed',
            'visited',
            'text',
            'page_title',
            'meta_title',
            'meta_description',
            'on_page_urls',
            'processed_urls',
        } == set(response.keys())

    @pytest.mark.asyncio
    @patch('logic.spiders.asynchronous.AsyncSpider.get')
    async def test_async_spider_request_method_returns_desired_data_for_wrong_status_codes(
        self, mock_get, spider, example_url_object,
    ):
        """
        Test that AsyncSpider request method is returning desired response
            when status codes are not in 200 or 300 range.
        """
        mock_response = MagicMock(spec=Response, status_code=404)
        mock_response.text = ''
        mock_response.url = example_url_object.value
        mock_response.elapsed = timedelta(10)
        mock_response.headers = {'server': 'test_server'}
        mock_get.return_value = mock_response, example_url_object
        response = await spider.request(spider.initial_url)
        mock_get.assert_called_once()

        assert isinstance(response, dict)
        assert {
            'requested_url',
            'responded_url',
            'status',
            'server',
            'elapsed',
            'visited',
        } == set(response.keys())

    @pytest.mark.asyncio
    @patch('logic.spiders.asynchronous.AsyncSpider.get')
    async def test_async_spider_request_method_returns_desired_data_for_none_response(
        self, mock_get, spider, example_url_object,
    ):
        """
        Test that AsyncSpider request method is returning desired response when response is None.
        """
        mock_get.return_value = None, example_url_object
        response = await spider.request(spider.initial_url)
        mock_get.assert_called_once()

        assert isinstance(response, dict)
        assert {'requested_url', 'status'} == set(response.keys())
        assert response['status'] is None

    @pytest.mark.asyncio
    @patch('logic.spiders.asynchronous.AsyncSpider.request')
    async def test_async_spider_run_requests_method_is_returning_expected_responses(
        self,
        mock_request,
        spider,
        example_url_objects,
    ):
        """Test that AsyncSpider request method is returning expected list of results."""
        responses = await spider.run_requests(example_url_objects)
        expected = [
            call(url=Url('http://found.onion/page0')),
            call(url=Url('http://found.onion/page1')),
            call(url=Url('http://found.onion/page2')),
            call(url=Url('http://found.onion/page3')),
            call(url=Url('http://found.onion/page4')),
        ]
        assert mock_request.mock_calls == expected

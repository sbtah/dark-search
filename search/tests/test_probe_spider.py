"""
Test cases for SyncSpider class.
"""
from unittest.mock import MagicMock, patch

import pytest
from httpx import ConnectTimeout, HTTPError, Response
from logic.spiders.probe import Probe

from search.logic.objects.url import Url


@pytest.fixture
def spider(example_url_object):
    """Fixture returning an instance of SyncSpider class."""
    spider = Probe(
        task_id=0,
        initial_url=example_url_object,
        proxy='http://test:8118',
        user_agent='Mozilla/Test',
        sleep_time=1,
        max_retries=4,
        timeout_time=60,
    )
    spider.logger = MagicMock()
    return spider


class TestSyncSpiderV2:
    """Test cases for Newer version of SyncSpider"""

    @patch('logic.spiders.synchronousv2.httpx.Client.get')
    def test_sync_spider_v2_get_method_is_successful(
        self,
        mock_get,
        spider,
        example_text_response,
        example_url_object,
    ) -> None:
        """Test that SyncSpider get method returns and behaves as expected."""
        assert example_url_object.number_of_requests == 0

        mock_response: MagicMock = MagicMock(status_code=200)
        mock_get.return_value = (mock_response, example_url_object)
        response = spider.get(url=spider.initial_url)
        mock_get.assert_called_once()

        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[1].number_of_requests == 1

    @patch('logic.spiders.synchronousv2.httpx.Client.get')
    def test_sync_spider_v2_get_method_conn_timeout_exception(
        self,
        mock_get,
        spider,
        example_url_object
    ) -> None:
        """Test that SyncSpider get method is increasing timeout attribute on ConnectionTimeout."""
        assert example_url_object.number_of_requests == 0
        assert spider.timeout_time == 60

        mock_get.side_effect = ConnectTimeout('Timed Out!')
        response = spider.get(url=spider.initial_url)
        mock_get.assert_called_once()

        assert example_url_object.number_of_requests == 1
        assert spider.timeout_time == 80
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[0] is None

    @patch('logic.spiders.synchronousv2.httpx.Client.get')
    def test_sync_spider_v2_get_method_returns_none_on_exception(
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

    # @patch('logic.spiders.synchronousv2.time.sleep')
    @patch('logic.spiders.synchronousv2.httpx.Client.get')
    def test_sync_spider_v2_run_request_method_is_successful(
        self,
        mock_get,
        spider,
        example_url_object,
    ) -> None:
        """
        Test that SyncSpider run_request method is returning expected data on success.
        Test logic of increasing number_of_requests on Url object.
        """
        assert example_url_object.number_of_requests == 0

        mock_response = MagicMock(spec=Response, status_code=200)
        mock_get.return_value = mock_response
        response = spider.run_request(url=example_url_object)

        mock_get.assert_called_once()
        assert example_url_object.number_of_requests == 1
        assert isinstance(response, tuple)

    @patch('logic.spiders.synchronousv2.time.sleep')
    @patch('logic.spiders.synchronousv2.httpx.Client.get')
    def test_sync_spider_v2_run_request_method_fails(
        self,
        mock_get,
        mock_sleep,
        spider,
    ) -> None:
        """
        Test that SyncSpider run_request will retry getting the url
            as long as url.number_of_request < max_retries.
        """
        example_url_object = Url(value='http://found-new.onion/')
        assert example_url_object.number_of_requests == 0

        mock_response = MagicMock(spec=Response, status_code=200)
        mock_get.return_value = mock_response
        mock_get.side_effect = (
            [None],
        )
        response = spider.run_request(url=example_url_object)

        assert mock_get.call_count == 4
        assert example_url_object.number_of_requests == 4
        assert isinstance(response, tuple)

    @patch('logic.spiders.synchronousv2.time.sleep')
    @patch('logic.spiders.synchronousv2.httpx.Client.get')
    def test_sync_spider_v2_run_request_method_is_retries_successful(
        self,
        mock_get,
        mock_sleep,
        spider,
    ) -> None:
        """
        Test SyncSpider run_request retry logic ends with success.
        """
        example_url_object = Url(value='http://found-new.onion/')
        assert example_url_object.number_of_requests == 0

        mock_response = MagicMock(spec=Response, status_code=200)
        mock_get.return_value = mock_response

        mock_get.side_effect = (
            [None] * 2 + [mock_response]
        )
        response = spider.run_request(url=example_url_object)
        assert mock_get.call_count == 3
        assert example_url_object.number_of_requests == 3
        assert isinstance(response, tuple)

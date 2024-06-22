from unittest.mock import MagicMock, patch

import pytest
from httpx import HTTPError, Response
from logic.spiders.synchronous import SyncSpider


class TestSyncSpider:
    @patch("logic.spiders.synchronous.httpx.Client.get")
    def test_sync_spider_get_method_returns_response_and_url_object(
        self,
        mock_get,
        example_text_response,
        example_url_object,
    ):
        """Test that SyncSpider get method is returning tuple with Response object and Url object."""
        mock_response = MagicMock(spec=Response, status_code=200)
        mock_get.return_value = (mock_response, example_url_object)

        spider = SyncSpider(
            initial_url=example_url_object,
            proxy="http://test:8118",
            user_agent="Mozilla/Test",
        )
        response = spider.get(url=spider.initial_url)
        mock_get.assert_called_once()
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[1].number_of_requests == 1

    @patch("logic.spiders.synchronous.httpx.Client.get")
    def test_sync_spider_get_method_returns_none_on_exception(
        self, mock_get, example_url_object
    ):
        """Test that SyncSpider get method is returning tuple with None and Url object on exception."""
        mock_get.side_effect = HTTPError("Error!")

        spider = SyncSpider(
            initial_url=example_url_object,
            proxy="http://test:8118",
            user_agent="Mozilla/Test",
        )
        response = spider.get(url=spider.initial_url)
        mock_get.assert_called_once()
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[1].number_of_requests == 1
        assert response[0] is None

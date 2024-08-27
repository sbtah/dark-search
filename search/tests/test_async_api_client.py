"""
Test cases for AsyncApiClient class.
"""
from unittest.mock import MagicMock, patch

import pytest
from httpx import Response
from logic.client.asynchronous import AsyncApiClient
from logic.objects.url import Url


@pytest.fixture
def example_token() -> str:
    return 'TEST_AUTH_TOKEN'


@pytest.fixture
def example_endpoint_url() -> Url:
    return Url('http://api.com/endpoint')


@pytest.fixture
def client() -> AsyncApiClient:
    """Fixture returning an instance of AsyncApiClient class."""
    return AsyncApiClient()


class TestAsyncApiClient:
    """
    Tests for AsyncApiClient functionality.
    """

    def test_prepare_headers_method(self, example_token, client) -> None:
        """
        Test that prepare_auth_headers method is creating expected dictionary.
        """
        client.api_key = example_token
        headers = client.prepare_headers()
        assert headers['Authorization'] == 'Token TEST_AUTH_TOKEN'

    @pytest.mark.asyncio
    @patch('logic.client.asynchronous.httpx.AsyncClient.get')
    async def test_async_api_client_get_method_returns_response_and_url_object(
        self,
        mock_get,
        client,
        example_endpoint_url,
    ) -> None:
        """
        Test that AsyncApiClient get method is returning expected response.
        """
        mock_response = MagicMock(spec=Response, status_code=200)
        mock_get.return_value = mock_response, example_endpoint_url

        response = await client.get(url=example_endpoint_url)
        mock_get.assert_called_once()
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert response[1].number_of_requests == 1

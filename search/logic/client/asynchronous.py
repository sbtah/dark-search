import asyncio
import json

import httpx
from httpx import Response
from logic.client.base import BaseClient
from logic.parsers.objects.url import Url


class AsyncApiClient(BaseClient):
    """
    Client class used in asynchronous communication with API service.
    """

    def __init__(self, *args, **kwargs) -> None:
        self._client: httpx.AsyncClient | None = None
        super().__init__(*args, **kwargs)

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient
        return self._client

    async def get(self, url: Url) -> tuple[Response | None, Url]:
        """
        Send GET requests to url value in Url object.
        Return tuple with Response object and Url object on success.
        - :arg url: Url object representing requsted endpoint.
        """
        headers = self.prepare_auth_headers()
        url.number_of_requests += 1
        try:
            async with self.client(
                limits=httpx.Limits(max_connections=1),
                timeout=httpx.Timeout(5),
                follow_redirects=False,
            ) as client:
                res = await client.get(url.value, headers)
                return res, url
        except Exception as exc:
            self.logger.error(
                f'{AsyncApiClient.get.__qualname__}: exception="{exc.__class__}", message="{exc}"'
            )
            return None, url

    async def post(self, url: Url, data: dict) -> tuple[Response | None, Url]:
        """
        Send POST request to value of Url object.
        Return tuple with Response and Url objects on success.
        - :arg url: Url object.
        - :data: Dictionary with data payload.
        """
        headers = self.prepare_auth_headers()
        url.number_of_requests += 1
        try:
            async with self.client(
                limits=httpx.Limits(max_connections=1),
                timeout=httpx.Timeout(5),
                follow_redirects=False,
            ) as client:
                res = await client.post(
                    url.value, headers, json=json.dumps(data)
                )
                return res, url
        except Exception as exc:
            self.logger.error(
                f'{AsyncApiClient.post.__qualname__}: exception="{exc.__class__}", message="{exc}"'
            )
            return None, url

    async def run_request(
        self, type: str, url: Url, data: dict | None = None
    ) -> tuple[Response | None, Url]:
        """
        Create an asyncio task for GET or POST request to endpoint specified via Url object.
        - :arg type: String representing a request method. Ie: 'POST' or 'GET'
        - :arg url: Url object with requested endpoint.
        - :arg data: Dictionary with data for POST request.
        """
        if type == 'GET':
            while True:
                async with asyncio.TaskGroup() as tg:
                    task = tg.create_task(self.get(url=url))
                    response = task.result()
                    if response[0] is None and url.number_of_requests < self.max_retries:
                        continue
                    if response[0] is not None:
                        return response

        if type == 'POST':
            while True:
                async with asyncio.TaskGroup() as tg:
                    task = tg.create_task(self.post(url=url, data=data))
                    response = task.result()
                    if response[0] is None and url.number_of_requests < self.max_retries:
                        continue
                    if response[0] is not None:
                        return response


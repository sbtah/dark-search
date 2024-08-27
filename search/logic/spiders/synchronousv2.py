import time

import httpx
from httpx import ConnectTimeout, Response
from logic.objects.url import Url
from logic.spiders.basev2 import BaseSpider


class SyncSpider(BaseSpider):
    """Synchronous base spider."""

    def __init__(self, *args, **kwargs) -> None:
        self._client: httpx.Client | None = None
        super().__init__(*args, **kwargs)

    def prepare_client_params(self) -> dict:
        """
        Prepare parameters for instance of httpx Client to be initialized with.
        Return prepared dictionary.
        """
        params = {
            'verify': False,
            'follow_redirects': self.follow_redirects,
        }

        if self.proxy is not None:
            proxy: str = self.proxy
            params['proxy'] = proxy

        if self.timeout_time is not None:
            timeout: httpx.Timeout = httpx.Timeout(self.timeout_time)
            params['timeout'] = timeout

        if self.max_requests is not None:
            max_requests: int = self.max_requests
            params['limits'] = max_requests
        return params

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client: httpx.Client = httpx.Client
        return self._client

    def get(self, *, url: Url) -> tuple[Response | None, Url]:
        """
        Send request to Url.value.
        Return tuple with Response object and Url object on success.
        - :arg url: Url object.
        """
        # Prepare headers, increase number_of_requests on Url object.
        headers: dict = self.prepare_headers()
        print(headers)
        url.number_of_requests += 1

        try:
            with self.client(**self.prepare_client_params()) as client:
                # Start measuring response time for url.
                request_start: int = self.now_timestamp()

                # Send the request.
                res: Response = client.get(url.value, headers=headers)

                # Calculate response time for Url.
                request_end: int = self.now_timestamp()
                current_response_time: int = request_end - request_start

                # Attach/monkeypatch response time value to Response object.
                setattr(res, 'current_response_time', current_response_time)

                return res, url
        except ConnectTimeout as cxc:
            # Increase time to timeout.
            self.timeout_time += 20

            self.logger.error(
                f'({SyncSpider.get.__qualname__}): exception="{cxc.__class__}", '
                f'message="{cxc}", task_id="{self.task_id}", '
                f'url="{url.value}"', exc_info=True,
            )
            return None, url
        except Exception as exc:
            self.logger.error(
                f'({SyncSpider.get.__qualname__}): exception="{exc.__class__}", '
                f'message="{exc}", task_id="{self.task_id}", '
                f'url="{url}"', exc_info=True,
            )
            return None, url

    def run_request(self, *, url: Url) -> tuple[Response | None, Url]:
        """
        Send get request to provided url.
        If response is not successful retry request up to self.max_retries.
        - :arg url: Url object.
        """
        while url.number_of_requests < self.max_retries:
            # Send a get request to provided Url.
            # Number of requests is increased in get method.
            response: tuple[Response | None, Url] = self.get(url=url)

            if response[0] is None:
                self.logger.debug(
                    f'({SyncSpider.run_request.__qualname__}): success="False", '
                    f'url="{url.value}", '
                    f'retry="{url.number_of_requests + 1}"'
                )
                time.sleep(self.sleep_time)
                continue

            if response[0] is not None and isinstance(response[0], Response):
                self.logger.debug(
                    f'({SyncSpider.run_request.__qualname__}): success="True", '
                    f'url="{url.value}", '
                    f'attempts="{url.number_of_requests}"'
                )
                return response
        else:
            return None, url

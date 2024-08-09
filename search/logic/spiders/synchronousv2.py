import httpx
import time
from httpx import Response, ConnectTimeout
from logic.objects.url import Url
from logic.spiders.basev2 import BaseSpider


class SyncSpider(BaseSpider):
    """Synchronous base spider."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get(self, *, url: Url) -> tuple[Response | None, Url]:
        """
        Send request to Url.value.
        Return tuple with Response object and Url object on success.
        - :arg url: Url object.
        """
        # Prepare headers, increase number_of_requests on Url object.
        headers: dict = self.prepare_headers()
        url.number_of_requests += 1

        # Setting initial variables for calculating response time.
        request_start: int | None = None
        request_end: int | None = None
        current_response_time: int | None = None

        try:
            with httpx.Client(
                verify=False,
                timeout=httpx.Timeout(self.timeout_time),
                follow_redirects=True,
                proxy=self.proxy,
            ) as client:
                # Start measuring response time for url.
                request_start = self.now_timestamp()

                # Send the request.
                res: Response = client.get(url.value, headers=headers)

                # Calculated response time for Url.
                request_end = self.now_timestamp()
                current_response_time = request_end - request_start

                # Attaching/monkeypatching response time value to Response object.
                res.current_response_time = current_response_time

                return res, url
        except ConnectTimeout as cxc:
            # Increasing time to timeout.
            self.timeout_time += 20

            self.logger.error(
                f'({SyncSpider.get.__qualname__}): exception="{cxc.__class__}", '
                f'message="{cxc}"', exc_info=True,
            )
            return None, url
        except Exception as exc:
            self.logger.error(
                f'({SyncSpider.get.__qualname__}): exception="{exc.__class__}", '
                f'message="{exc}"', exc_info=True,
            )
            return None, url

    def run_request(self, *, url: Url) -> tuple[Response | None, Url]:
        """
        Send get request to provided url.
        If response is not successful retry request up to self.max_retries.
        - :arg url: Url object.
        """
        while url.number_of_requests < self.max_retries:
            # Sending a get request to provided Url.
            # Number of requests is increased in get method.
            response: tuple[Response | None, Url] = self.get(url=url)

            if response[0] is None:
                self.logger.debug(
                    f'({SyncSpider.run_request.__qualname__}): success="False", '
                    f'retry="{url.number_of_requests + 1}", '
                )
                time.sleep(self.sleep_time)
                continue

            if response[0] is not None and isinstance(response[0], Response):
                self.logger.debug(
                    f'({SyncSpider.run_request.__qualname__}): success="True", '
                    f'attempts="{url.number_of_requests}", '
                )
                return response
        else:
            return None, url

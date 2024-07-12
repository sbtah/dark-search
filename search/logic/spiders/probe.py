from collections import deque

from logic.parsers.objects.url import Url
from logic.spiders.synchronous import SyncSpider


class Probe(SyncSpider):
    """
    Probing spider used for first request.
    Saves initial data for requested domain.
    Extracts urls that will be provided to Crawler.
    """

    def __init__(self, max_retries: int = 4, *args, **kwargs) -> None:
        self.max_retries: int = max_retries
        self.queue: deque[Url] = deque()
        super().__init__(*args, **kwargs)

    def probe(self):
        """
        Send probing request to initial_url.
        """

        self.logger.info(f'Probe Start: domain="{self.domain}", url="{self.initial_url}"')

        self.prepare_urls_queue()

        while len(self.queue) > 0:

            # Run requests for url in the queue.
            response: dict = self.request()

            if response['status'] is None and response['requested_url'].number_of_requests < self.max_retries:
                continue

            # TODO:
            # Work on API client.
            # Url object must be serialized to dict...
            # self.client.post_response_data(data=response)
            return response

    def prepare_urls_queue(self) -> None:
        """
        Add initial_url to Queue.
        """
        self.queue.append(self.initial_url)
        return

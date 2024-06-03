from collections import deque
from typing import Collection

from logic.objects.url import Url
from logic.spiders.asynchronous import AsyncSpider


class Crawler(AsyncSpider):
    """
    Asynchronous Crawler.
    Integrates async requests and sending crawled/scraped data to API.
    """

    def __init__(self, urls_to_crawl: Collection[Url], max_retries: int = 4, *args, **kwargs):
        self.urls_to_crawl: Collection[Url] = urls_to_crawl
        self.max_retries: int = max_retries
        self.queue: deque[Url] = deque()
        self.found_internal_urls: set[Url | None] = set()
        self.requested_urls: set[Url | None] = set()
        self.external_domains: set[Url | None] = set()
        self.crawl_start: int = self.now_timestamp()
        self.crawl_end: int | None = None
        super().__init__(*args, **kwargs)

    async def start_crawling(self) -> None:
        """Initiate a crawling process for urls in self.urls_to_crawl Collection."""
        self.logger.info(f'Crawl Start: domain="{self.domain}"')
        self.found_internal_urls.add(*self.urls_to_crawl)
        await self.crawl()

    async def crawl(self) -> None:
        """
        Crawling proces that travel trough domain and looks for urls.
        Found urls are filtered to internal urls and external domains.
        External domains are being saved with proper Task.
        Internal urls are added to found_internal_urls for further crawling.
        """

        while len(self.found_internal_urls) > 0:
            self.logger.info(
                f'Crawl: domain="{self.domain}" urls_to_crawl="{len(self.found_internal_urls)}" found_domains="{len(self.external_domains)}"'
            )
            self.prepare_urls_queue()

            # Run requests for urls in the queue...
            responses: list[Exception | dict] = await self.run_requests(iterable_of_urls=self.queue)

            for response in responses:

                # If response is None and Url.number_of_request is under max_retries threshold,
                #   we want to keep this Url in the found_internal_urls set.
                if response['status'] is None and response['requested_url'].number_of_requests < self.max_retries:
                    continue

                # Add url to the requested_urls set and remove from found_internal_urls if request was successful.
                self.requested_urls.add(response['requested_url'])
                self.found_internal_urls.remove(response['requested_url'])

                # TODO:
                # Work on API client.
                # await is blocking should we create_task here?
                # Url object must be serialized to dict...
                # await self.client.post_response_data(data=response)

                # If both sets in processed_urls are empty we move to next response.
                if not response.get('processed_urls', {}).get('internal') and not response.get('processed_urls', {}).get('external'):
                    continue

                # Parsing results of newly found external domains.
                for domain in response.get('processed_urls').get('external'):
                    if domain not in self.external_domains:
                        self.external_domains.add(domain)
                        # self.logger.debug(
                        #     f'Response: new_external_domain="{domain}" at url="{response['requested_url']}"'
                        # )
                        # TODO
                        # Implement this logic in adapter.
                        # await is blocking should we create_task here?
                        # await self.task_adapter.get_or_create_task(domain=domain)

                # Add results from internal results set to found_internal_urls.
                for url in response.get('processed_urls').get('internal'):
                    # If an url was not requested already or is not waiting to be requested,
                    #   we want to add it to the found_internal_urls set.
                    if url not in self.requested_urls and url not in self.found_internal_urls:
                        self.found_internal_urls.add(url)
                        # self.logger.debug(
                        #     f'Response: new_internal_url="{url}" at url="{response['requested_url']}"'
                        # )
            else:
                # Clear the queue.
                self.queue.clear()
        else:
            self.logger.info(
                f'Crawl Finished: domain="{self.domain}" crawled_urls="{len(self.requested_urls)}" found_domains="{len(self.external_domains)}"'
            )
            # TODO:
            # Work on API client.
            # await is blocking should we create_task here?
            # await self.client.post_summary_data(
            #     data={
            #         'domain': self.initial_domain,
            #         'urls_crawled': len(self.requested_urls),
            #         'time': self.crawl_end - self.crawl_start,
            #         'date': self.now_timestamp()
            #     }
            # )
            return

    def prepare_urls_queue(self) -> None:
        """
        Add found urls to Queue up to max_requests limit.
        """
        for url in self.found_internal_urls:
            if len(self.queue) < self.max_requests:
                self.queue.append(url)
        return

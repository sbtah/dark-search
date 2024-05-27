from collections import deque
from typing import Collection

from logic.spiders.asynchronous import AsyncSpider


class Crawler(AsyncSpider):
    """
    Asynchronous Crawler.
    Integrates async requests and sending crawled/scraped data to API.
    """

    def __init__(self, urls_to_crawl: Collection, *args, **kwargs):
        self.urls_to_crawl: Collection[str] = urls_to_crawl
        self.queue: deque[str] = deque()
        self.found_internal_urls: set[str | None] = set()
        self.requested_urls: set[str | None] = set()
        self.external_domains: set[str | None] = set()
        self.crawl_start: int = self.now_timestamp()
        self.crawl_end: int | None = None
        super().__init__(*args, **kwargs)

    async def start_crawling(self) -> None:
        """Initiate a crawling process for urls in self.urls_to_crawl Collection."""
        self.logger.info(f'Crawl Start: domain="{self.domain}"')
        self.found_internal_urls.add(*self.urls_to_crawl)
        await self.crawl()

    async def crawl(self):
        """
        Crawling proces that travel trough domain recursively and looks for urls.
        Found urls are filtered to internal urls and external domains.
        External domains are being saved with proper Task.
        Internal urls are added to found_internal_urls for further crawling.
        """
        self.logger.info(
            f'Crawl: domain="{self.domain}" urls_to_crawl="{len(self.found_internal_urls)}" found_domains="{len(self.external_domains)}"'
        )
        self.prepare_urls_queue()

        responses = await self.run_requests(iterable_of_urls=self.queue)

        for response in responses:
            print(response)

            # Add url to the requested_urls set and remove from found_internal_urls if request was successful.
            self.requested_urls.add(response['requested_url'])
            self.found_internal_urls.remove(response['requested_url'])

            # TODO:
            # Work on API client.
            # await self.client.post_response_data(data=response)

            # self.logger.info(
            #     f"Received response from: - {response['requested_url']}"
            # )
            # Parsing processed_urls result.
            if not response.get('processed_urls', {}).get('internal') and not response.get('processed_urls', {}).get('external'):
                continue
            
            # Parsing results of found external domains.
            for domain in response.get('processed_urls').get('external'):
                if domain not in self.external_domains:
                    self.external_domains.add(domain)
                    # TODO
                    # Implement this logic in adapter.
                    # 
                    # await self.task_adapter.get_or_create_task(domain=domain)

            # Add results from internal results set to found_internal_urls.
            for url in response.get('processed_urls').get('internal'):
                # If an url was not requested already or is not waiting to be requested,
                #   we want to add it to the found_internal_urls set.
                if url not in self.requested_urls and url not in self.found_internal_urls:
                    self.found_internal_urls.add(url)
        else:
            # Clear the queue.
            self.queue.clear()

        if not self.found_internal_urls:
            self.logger.info(
                f'Crawl Finished: domain="{self.domain}" crawled_urls="{len(self.requested_urls)}" found_domains="{len(self.external_domains)}"'
            )
            
            # TODO:
            # Work on API client.
            # await self.client.post_summary_data(
            #     data={
            #         'domain': self.initial_domain,
            #         'urls_crawled': len(self.requested_urls),
            #         'time': self.crawl_end - self.crawl_start,
            #         'date': self.now_timestamp()
            #     }
            # )
            return
        else:
            await self.crawl()

    def prepare_urls_queue(self) -> None:
        """
        Add found urls to Queue up to max_requests limit.
        """
        for url in self.found_internal_urls:
            if len(self.queue) < self.max_requests:
                self.queue.append(url)
        return

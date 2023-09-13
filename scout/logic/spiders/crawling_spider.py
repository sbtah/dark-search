from urllib.parse import urlsplit
import time
from logic.spiders.async_spider import AsyncSpider


class Crawler(AsyncSpider):

    def __init__(self, crawl_type: str, initial_url: str, initial_domain: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crawl_type = crawl_type
        self.initial_url = initial_url
        self.initial_domain = initial_domain
        self.found_urls = {initial_url,}
        self.external_domains = set()
        self.requested_urls = set()
        self.max_requests = 10
        self.sleep_time = 10
        self.site_structure = {}
        self.logger.info(f'Starting crawler for: {initial_url}')

    async def crawl(self):
        """
        Crawling process that just discovers all urls on specified domain.
        """

        self.logger.info(f'CRAWLING: {len(self.found_urls)} new URLs to crawl at: {self.initial_domain}')
        # Here I'm basically ratelimiting number on concurrent requests to self.max_requests.
        lists_of_urls_list = await self.ratelimit_urls(list(self.found_urls))

        for list_of_urls in lists_of_urls_list:
            responses = await self.get_requests(iterator_of_urls=list_of_urls)

            for response in responses:

                self.requested_urls.add(response['requested_url'])
                self.found_urls.remove(response['requested_url'])

                if response['status'] is not None:
                    self.logger.info(f'PROCESSING: Received response from: {response["requested_url"]}')
                    # Sending prepared successful response data to API.
                    await self.client.post_response_data(data=response)
                    # Filter found urls found on requested page.
                    if response.get('processed_urls') is not None:
                        # Schedule and save urls accordingly.
                        processed_urls = response['processed_urls']
                        # Filtering urls to internal/external_domains.
                        filtered = await self.filter_found_urls(processed_urls=processed_urls)

                        new_external_domains = filtered['external_domains']
                        internal_urls = filtered['internal_urls']
                        # Here we push newly found internal urls to queue.
                        self.found_urls.update(internal_urls)
                        # External domains are processed here.
                        if new_external_domains:
                            for domain in new_external_domains:
                                if domain not in self.external_domains:
                                    self.logger.info(f'SAVING: Potential new domain found: {domain}')
                                    await self.domain_adapter.get_or_create_domain(domain=domain)
                            self.external_domains.update(new_external_domains)
                else:
                    self.logger.info(f"PASSING: Received no response from: {response['requested_url']}")
        if self.found_urls:
            await self.crawl()
        else:
            self.logger.info(f'FINISHED: No more URLs to crawl at: {self.initial_domain}')
            return

    async def ratelimit_urls(self, urls):
        """
        My implementation of limiting number of requests send.
        I'm simply splitting received iterator of urls to list of list with length of self.max_requests.
        Generate list of urls lists.
        """
        self.max_requests
        if len(urls) > self.max_requests:
            return [
                urls[x : x + self.max_requests] for x in range(0, len(urls), self.max_requests)
            ]
        else:
            return [urls, ]

    async def filter_found_urls(self, processed_urls: list):
        """
        Takes list of proccesed url
        """
        filtered = {'internal_urls': set(), 'external_domains': set()}
        for url in processed_urls:
            if self.initial_domain in url and url not in self.requested_urls:
                filtered['internal_urls'].add(url)
            elif self.initial_domain not in url and url not in self.requested_urls:
                filtered['external_domains'].add(urlsplit(url).netloc)
        return filtered

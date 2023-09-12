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
        self.logger.info(f'CRAWLING: {len(self.found_urls)} new URLs to crawl at: {self.initial_domain}.')
        lists_of_urls_list = self.ratelimit_urls(list(self.found_urls))

        for list_of_urls in lists_of_urls_list:
            responses = await self.get_requests(iterator_of_urls=list_of_urls)
            for response in responses:
                self.logger.info(f'Processing response from: {response["requested_url"]}.')
                self.requested_urls.add(response['requested_url'])
                self.found_urls.remove(response['requested_url'])
                if response['status'] is not None:
                    await self.client.post_response_data(data=response)
                    if response.get('processed_urls') is not None:
                        # Schedule and save urls accordingly.
                        processed_urls = response['processed_urls']
                        filtered = self.filter_found_urls(processed_urls=processed_urls)
                        external_domains = filtered['external_domains']
                        internal_urls = filtered['internal_urls']
                        self.found_urls.update(internal_urls)
                        if external_domains:
                            self.logger.info(f'Found {len(external_domains)} new domains.')
                            for domain in external_domains:
                                self.logger.info(f'Saving new Domain: {domain}')
                                await self.domain_adapter.get_or_create_domain(domain=domain)
                else:
                    self.logger.info(f"No response from: {response['requested_url']}")
        if self.found_urls:
            await self.crawl()
        else:
            self.logger.info(f'FINISHED: No more URLs to crawl at: {self.initial_domain}.')
            return


    def ratelimit_urls(self, urls):
        """
        My implementation of limiting number of requests send.
        Im simply spliting received iterator of urls to list of list with length of self.max_requests.
        Generate list of urls lists.
        """
        self.max_requests
        if len(urls) > self.max_requests:
            return [
                urls[x : x + self.max_requests] for x in range(0, len(urls), self.max_requests)
            ]
        else:
            return [urls, ]

    def filter_found_urls(self, processed_urls):
        """"""
        filtered = {'internal_urls': set(), 'external_domains': set()}
        for url in processed_urls:
            if self.initial_domain in url and url not in self.requested_urls:
                filtered['internal_urls'].add(url)
            elif self.initial_domain not in url and url not in self.requested_urls:
                filtered['external_domains'].add(urlsplit(url).netloc)
        return filtered

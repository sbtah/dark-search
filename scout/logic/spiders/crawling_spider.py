from urllib.parse import urlsplit
from logic.spiders.async_spider import AsyncSpider


class Crawler(AsyncSpider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    async def start_crawling(self):
        self.found_internal_urls.add(self.initial_url)
        await self.crawl()

    async def crawl(self):
        """
        Crawling process that travels trough domain recursively and looks for urls.
        Found urls are filtered to internal urls and external domains.
        External domains are being saved with proper Task.
        Internal urls are added to found_internal_urls for further crawling.
        """

        self.logger.info(
            f"""
                Crawling: {self.initial_domain}
                Found: {len(self.found_internal_urls)} url(s).
            """
        )
        lists_of_urls_list = await self.ratelimit_urls(list(self.found_internal_urls))

        for list_of_urls in lists_of_urls_list:
            responses = await self.get_requests(iterator_of_urls=list_of_urls)

            for response in responses:

                self.requested_urls.add(response['requested_url'])
                self.found_internal_urls.remove(response['requested_url'])

                await self.client.post_response_data(data=response)

                if response['status'] is not None:
                    self.logger.info(
                        f"""
                            Received response from: 
                                - {response['requested_url']}
                        """
                    )
                    if response.get('processed_urls') is not None:
                        filtered = await self.filter_processed_urls(
                            processed_urls=response['processed_urls']
                        )
                        new_external_domains = filtered['external_domains']
                        internal_urls = filtered['internal_urls']
                        await self.process_filtered(
                            internal_urls=internal_urls,
                            external_domains=new_external_domains,
                        )
                    else:
                        self.logger.info(
                            f"""
                                No processed urls at: 
                                    - {response['requested_url']}
                            """
                        )
                        continue
                else:
                    self.logger.info(
                        f"""
                            Received no response from:
                                - {response['requested_url']}
                        """
                    )
                    continue
        if self.found_internal_urls:
            await self.crawl()
        else:
            self.logger.info(
                f"""
                    No more urls to crawl at: {self.initial_domain}.
                    Requested {len(self.requested_urls)} urls.
                """
            )
            return

    async def ratelimit_urls(self, urls):
        """
        My implementation of limiting number of requests send.
        I'm simply splitting received iterator of urls,
            to list of list with length of self.max_requests.
        Generate list of urls lists.
        """

        if len(urls) > self.max_requests:
            return [
                urls[x: x + self.max_requests] for x in range(0, len(urls), self.max_requests)
            ]
        else:
            return [urls, ]

    async def filter_processed_urls(self, processed_urls: list):
        """
        Takes list of processed urls and filters in into 2 sets:
        internal_urls and external_domains.
        """

        filtered = {'internal_urls': set(), 'external_domains': set()}
        for url in processed_urls:
            if self.initial_domain in url and url not in self.requested_urls:
                filtered['internal_urls'].add(url)
            elif self.initial_domain not in url:
                filtered['external_domains'].add(urlsplit(url).netloc)
        return filtered

    async def process_filtered(
            self,
            internal_urls: set,
            external_domains: set = None,
    ):
        """
        Takes output sets from filter_processed_url,
        and add internal_urls to found_internal_urls.
        Unique external domains in 2nd set are saved in database.
        """
        # Here we push newly found internal urls to 'queue'.
        self.found_internal_urls.update(internal_urls)
        # External domains are processed here.
        if external_domains is not None:
            for domain in external_domains:
                if domain not in self.external_domains:
                    domain_object = await self.domain_adapter.get_or_create_domain(domain=domain)
                    await self.task_adapter.get_or_create_task(domain=domain_object)
            self.external_domains.update(external_domains)

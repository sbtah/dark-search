import asyncio
from logic.spiders.crawling_spider import Crawler



url = 'http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/'
domain = 'tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion'




async def crawler_test():
    # url_response = await TorScoutApiClient().get_not_crawled_website()
    # if url_response is not None:
    crawler = Crawler(crawl_type='SEARCH', initial_url=url, initial_domain=domain)
    await crawler.crawl()



if __name__ == '__main__':
    #sync_test()
    # out = asyncio.run(crawl_page(iterator_of_urls=urls))
    asyncio.run(crawler_test())
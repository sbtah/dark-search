import httpx
from httpx import Response
from logic.parsers.objects.url import Url
from logic.spiders.base import BaseSpider
from lxml.html import HtmlElement


class SyncSpider(BaseSpider):
    """Synchronous base spider."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get(self, url: Url) -> tuple[Response | None, Url]:
        """
        Send request to Url.value.
        Return tuple with Response object and Url object on success.
        - :arg url: Url object.
        """
        headers: dict = self.prepare_headers()
        url.number_of_requests += 1
        try:
            with httpx.Client(
                verify=False,
                timeout=httpx.Timeout(60.0),
                follow_redirects=True,
                proxy=self.proxy,
            ) as client:
                res = client.get(url.value, headers=headers)
                return res, url
        except Exception as exc:
            self.logger.error(f'({SyncSpider.get.__qualname__}): Some other exception: {exc}')
            return None, url

    def request(self, url: Url):
        """
        Request specified value in provided Url object.
        Return dictionary with needed data.
        :arg url: Url object.
        """

        # Response from requesting a webpage. HtmlElement generated from the response text.
        response: tuple[Response | None, Url] = self.get(url)
        element: HtmlElement | None = self.html_extractor.page(response[0]) if response[0] is not None else None

        try:
            if isinstance(response[0], Response):
                self.logger.debug(
                    f'Response: status="{response[0].status_code}", url="{url}", html="{True if element is not None else False}"'
                )
                if str(response[0].status_code)[0] in {'2', '3'} and element is not None:

                    # Parsing text prepared html element.
                    parse_html_results = self.html_extractor.parse(element)
                    # Parsing urls found on the webpage.
                    parse_urls_results = self.url_extractor.parse(parse_html_results['on_page_urls'])

                    # Preparing favicon url
                    favicon_url = parse_html_results['favicon_url']
                    split_result = self.url_extractor.split_result(favicon_url)
                    if not self.url_extractor.is_valid_url(split_result) and self.url_extractor.is_path(split_result.path):
                        favicon_url = self.url_extractor.join_result(self.initial_url.value, favicon_url)

                    return {
                        'requested_url': url,
                        'responded_url': str(response[0].url),
                        'status': str(response[0].status_code),
                        'server': response[0].headers.get('server', None),
                        'elapsed': str(response[0].elapsed.total_seconds()),
                        'visited': int(self.now_timestamp()),
                        'html': parse_html_results['html'],
                        'page_title': parse_html_results['page_title'],
                        'meta_title': parse_html_results['meta_title'],
                        'meta_description': parse_html_results['meta_description'],
                        'on_page_urls': parse_html_results['on_page_urls'],
                        'processed_urls': parse_urls_results,
                        'favicon_url': favicon_url,
                    }

                if str(response[0].status_code)[0] not in {'2', '3'}:
                    return {
                        'requested_url': url,
                        'responded_url': str(response[0].url),
                        'status': str(response[0].status_code),
                        'server': response[0].headers.get('server', None),
                        'elapsed': str(response[0].elapsed.total_seconds()),
                        'visited': int(self.now_timestamp()),
                    }

            if response[0] is None:
                    self.logger.debug(
                        f'Response: status="None", url="{url}", html="{True if element is not None else False}"'
                    )
                    return {
                        'requested_url': url,
                        'status': None,
                    }
        except Exception as e:
            self.logger.debug(
                f'Response: status="Exception: {e}", url="{url}", html="{True if element is not None else False}"'
            )
            return {
                'requested_url': url,
                'status': None,
            }

import httpx
from httpx import Response
from logic.objects.url import Url
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
            self.logger.error(
                f'({SyncSpider.get.__qualname__}): Some other exception="{exc.__class__}", '
                f'message="{exc}"', exc_info=True,
            )
            return None, url

    def request(self, url: Url = None) -> dict:
        """
        Request specified value of provided Url object.
        Return dictionary with needed data.
        :arg url: Url object.
        """
        # Setting url value.
        url = url if url is not None else self.initial_url

        # Start measuring response time for url.
        request_start: int = self.now_timestamp()

        # Response from requesting a webpage.
        response: tuple[Response | None, Url] = self.get(url)

        # Calculate time for response.
        request_end: int = self.now_timestamp()
        response_time: int = request_end - request_start

        # HtmlElement generated from the response text.
        element: HtmlElement | None = self.html_extractor.page(response[0]) if response[0] is not None else None

        try:
            if isinstance(response[0], Response):
                self.logger.debug(
                    f'Response: status="{response[0].status_code}", url="{url}", html="{True if element is not None else False}"'
                )
                if str(response[0].status_code)[0] in {'2', '3'} and element is not None:

                    # Parsing text prepared html element.
                    parse_html_results: dict = self.html_extractor.parse(element)
                    # Parsing urls found on the webpage.
                    parse_urls_results: dict = self.url_extractor.parse(parse_html_results['on_page_urls'])

                    # Preparing favicon url
                    favicon_url: str | None = parse_html_results['favicon_url']
                    favicon_url_obj: Url | None = self.url_extractor.parse_favicon_url(favicon_url)

                    return {
                        # Serialize me later...
                        'requested_url': url,
                        'status': str(response[0].status_code),
                        'responded_url': str(response[0].url),
                        'server': response[0].headers.get('server', None),
                        'content_type': response[0].headers.get('content-type'),
                        'response_time': response_time,
                        'visited': int(self.now_timestamp()),
                        'text': parse_html_results['text'],
                        'page_title': parse_html_results['page_title'],
                        'meta_title': parse_html_results['meta_title'],
                        'meta_description': parse_html_results['meta_description'],
                        'on_page_urls': parse_html_results['on_page_urls'],
                        'processed_urls': parse_urls_results,
                        # Serialize me later...
                        'favicon_url': favicon_url_obj,
                    }

                if str(response[0].status_code)[0] not in {'2', '3'} or element is None:
                    return {
                        'requested_url': url,
                        'status': str(response[0].status_code),
                        'responded_url': str(response[0].url),
                        'server': response[0].headers.get('server', None),
                        'content_type': response[0].headers.get('content-type'),
                        'response_time': response_time,
                        'visited': int(self.now_timestamp()),
                    }

            if response[0] is None:
                self.logger.debug(
                    f'Response: status="None", url="{url}", html="False"'
                )
                return {
                    'requested_url': url,
                    'status': None,
                }
        except Exception as e:
            self.logger.error(
                f'Response: status="Exception", class="{e.__class__}", message="{e}", '
                f'url="{url}"', exc_info=True
            )
            return {
                'requested_url': url,
                'status': None,
            }

    def request_favicon(self, favicon_url: Url) -> str | None:
        """
        Request Url object for favicon url.
        Return base64 representation of icon.
        - :arg favicon_url: Url object.
        """
        # Request favicon url.
        response: tuple[Response | None, Url] = self.get(url=favicon_url)
        # Process response to base64 string.
        favicon_base_64: str | None = self.converter.convert(response[0].content) if \
            response[0] is not None and str(response[0].status_code)[0] in {'2', '3'} else None
        return favicon_base_64

from logic.spiders.synchronousv2 import SyncSpider
from httpx import Response, ConnectTimeout
from logic.objects.url import Url
from lxml.html import HtmlElement


class Probe(SyncSpider):
    """
    Probing spider used for first request.
    Saves initial data for requested domain.
    Extracts urls that will be provided to Crawler.
    """

    def start_probing(self):
        """Initiate a probing process."""
        self.logger.info(f'Probe, initiated: domain="{self.domain}"')
        result: dict = self.probe()
        return result

    def probe(self, ) -> dict:
        """"""

        # Sending requests.
        response: tuple[Response, Url] | None = self.run_request(url=self.initial_url)

        # Parsing response.
        parsed_response: dict = self.parse_response(
            response_object=response, url=self.initial_url, response_time=self.current_response_time
        )

        # Processing favicon url.
        if parsed_response.get('favicon_url') is not None:
            favicon_url: Url = parsed_response['favicon_url']
            favicon_response = self.run_request(url=favicon_url)

    def parse_response(self, *, response_object: Response | None, url: Url, response_time: int) -> dict:
        """"""
        try:
            if response_object[0] is None:
                self.logger.debug(
                    f'Response: status="None", url="{url}", html="False"'
                )
                return {
                    'requested_url': url,
                    'status': None,
                }

            if str(response_object[0].status_code)[0] in {'2', '3'}:
                # Extracting html early.
                element: HtmlElement | None = self.html_extractor.page(response_object[0])

                # Extracting favicon url.
                favicon_url: str | None = self.html_extractor.extract_favicon_url(element)
                favicon_url_obj: Url | None = self.url_extractor.parse_favicon_url(favicon_url)

                self.logger.debug(
                    f'Parsing response: status="{response_object[0].status_code}", '
                    f'url="{url}", html="{True if element is not None else False}"'
                )

                prepared_response: dict = {
                    'requested_url': url,
                    'status': str(response_object[0].status_code),
                    'bytes_downloaded': response_object[0].num_bytes_downloaded,
                    'responded_url': str(response_object[0].url),
                    'server': response_object[0].headers.get('server', None),
                    'content_type': str(response_object[0].headers.get('content-type')),
                    'response_time': int(response_time),
                    'visited': int(self.now_timestamp()),
                    'favicon_url': favicon_url_obj,
                }
                return prepared_response

            if str(response_object[0].status_code)[0] not in {'2', '3'}:
                pass

        except Exception as e:
            self.logger.error(
                f'Parsing response: status="Exception", class="{e.__class__}", message="{e}", '
                f'url="{url}"', exc_info=True
            )
            return {
                'requested_url': url,
                'status': None,
            }

    def serialized_response(self):
        ...
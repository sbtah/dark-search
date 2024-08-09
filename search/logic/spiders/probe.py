from logic.spiders.synchronousv2 import SyncSpider
from httpx import Response, ConnectTimeout
from logic.objects.url import Url
from lxml.html import HtmlElement
import copy
from logic.schemas.url import UrlSchema


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

    def probe(self) -> dict:
        """"""
        # Send request to Url object that spider was initialed with.
        response: tuple[Response, Url] | None = self.run_request(url=self.initial_url)

        # Parse received response, extract data.
        parsed_response: dict = self.parse_response(response=response)

        # Serialize objects, prepare data to be sent to the API.
        serialized_response: dict = self.serialize_response()

        if parsed_response.get('favicon_url') is None:
            # TODO: Send data to the API.
            return parsed_response

        # Extracting favicon url.
        favicon_url: Url = parsed_response['favicon_url']

        favicon_response: tuple[Response | None, Url] = self.run_request(url=favicon_url)
        parsed_favicon_response: dict = self.parse_favicon_response(response=favicon_response)

        extended_serialized_response: dict = {
            **serialized_response,
            **parsed_favicon_response,
        }
        # TODO: Send extended data to the API.

        extended_response: dict = {
            **parsed_response,
            **parsed_favicon_response,
        }
        return extended_response

    def parse_response(self, *, response: tuple[Response | None, Url]) -> dict:
        """"""

        # Saving Url object from response.
        url: Url = response[1]

        try:
            if response[0] is None:
                self.logger.debug(
                    f'Parsing response: status="None", url="{url}", html="False"'
                )
                return {
                    'requested_url': url,
                    'status': None,
                }

            prepared_response: dict = {
                'requested_url': url,
                'status': str(response[0].status_code),
                'bytes_downloaded': response[0].num_bytes_downloaded,
                'responded_url': str(response[0].url),
                'server': response[0].headers.get('server', None),
                'content_type': str(response[0].headers.get('content-type')),
                'response_time': int(response[0].current_response_time),
                'date': self.now_timestamp(),
                'visited': int(self.now_timestamp()),
            }

            if str(response[0].status_code)[0] not in {'2', '3'}:
                return prepared_response

            if str(response[0].status_code)[0] in {'2', '3'}:
                # Extracting html element.
                element: HtmlElement | None = self.html_extractor.page(response[0])

                # Extracting favicon url.
                favicon_url: str | None = self.html_extractor.extract_favicon_url(element)
                favicon_url_obj: Url | None = self.url_extractor.parse_favicon_url(favicon_url)

                self.logger.debug(
                    f'Parsing response: status="{response[0].status_code}", '
                    f'url="{url}", html="{True if element is not None else False}"'
                )

                prepared_response['favicon_url'] = favicon_url_obj,
                return prepared_response

        except Exception as e:
            self.logger.error(
                f'Parsing response: status="Exception", class="{e.__class__}", message="{e}", '
                f'url="{url}"', exc_info=True
            )
            return {
                'requested_url': url,
                'status': None,
            }

    def parse_favicon_response(self, *, response: tuple[Response | None, Url]) -> dict:
        """"""

        # Saving Url object from response.
        url: Url = response[1]
        base_response: dict = {
            'favicon_base64': None,
        }
        try:
            if response[0] is None:
                self.logger.debug(
                    f'Parsing favicon response: status="None", url="{url}"'
                )
                return base_response

            if response[0].is_success is True:
                prepared_response: dict = {
                    'favicon_base64': self.converter.convert(response[0].content),
                }
                return prepared_response
            else:
                return base_response

        except Exception as e:
            self.logger.error(
                f'Parsing favicon response: status="Exception", class="{e.__class__}", message="{e}", '
                f'url="{url}"', exc_info=True
            )
            return base_response

    def serialize_response(self, response_dict: dict) -> dict:
        """

        """
        copied_response: dict = copy.deepcopy(response_dict)
        url: Url = copied_response.pop('requested_url')
        url_model: UrlSchema = UrlSchema.model_validate(url.serialize())
        url_dict: dict = url_model.model_dump()
        serialized_response: dict = {'requested_url': url_dict, **copied_response}

        if copied_response.get('favicon_url') is None:
            return serialized_response

        favicon_url: Url = copied_response.pop('favicon_url')
        favicon_url_model: UrlSchema = UrlSchema.model_validate(favicon_url.serialize())
        favicon_url_dict: dict = favicon_url_model.model_dump()
        serialized_response['favicon_url'] = favicon_url_dict

        if copied_response.get('favicon_base64') is None:
            return serialized_response

        serialized_response['favicon_base64'] = copied_response.get('favicon_base64')
        return serialized_response

import copy

from httpx import Response
from logic.objects.url import Url
from logic.schemas.url import UrlSchema
from logic.spiders.synchronousv2 import SyncSpider
from lxml.html import HtmlElement


class Probe(SyncSpider):
    """
    Probing spider used for first request.
    Saves initial data for requested domain.
    """

    def prepare_headers(self) -> dict:
        """Prepare request headers for next request."""
        assert self.user_agent is not None, f'Failed at preparing request headers: User Agent is: {self.user_agent}'
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'close',
            'User-Agent': self.user_agent,
        }

    def start_probing(self):
        """Initiate a probing process."""
        self.logger.info(f'Probe, initiated: task_id="{self.task_id}", domain="{self.domain}"')
        result: dict = self.probe()
        return result

    def probe(self) -> dict:
        """
        Send request to initial Url.
        Send post request to dedicated API endpoint with necessary data.
        Return dict with extracted data.
        """
        # Send request to Url object that spider was initialed with.
        response: tuple[Response, Url] | None = self.run_request(url=self.initial_url)

        # Parse received response, extract data.
        parsed_response: dict = self.parse_response(response=response)

        # TODO:
        # Serialize objects, prepare data to be sent to the API.
        serialized_response: dict = self.serialize_response(response_dict=parsed_response)

        if parsed_response.get('favicon_url') is None:
            self.logger.info(
                f'Probe, finished: task_id={self.task_id}, domain="{self.domain}"'
            )
            # TODO: Send data to the API.
            return parsed_response

        # Extract favicon url, run request for it. Parse response to base64 string.
        favicon_url: Url = parsed_response['favicon_url']
        favicon_response: tuple[Response | None, Url] = self.run_request(url=favicon_url)
        parsed_favicon_response: dict = self.parse_favicon_response(response=favicon_response)

        # Add data extracted from favicon parsing to serialized data.
        extended_serialized_response: dict = {
            **serialized_response,
            **parsed_favicon_response,
        }
        # TODO: Send extended data to the API.

        # Extend response with favicon in base64.
        extended_response: dict = {
            **parsed_response,
            **parsed_favicon_response,
        }
        self.logger.info(
            f'Probe, finished: task_id="{self.task_id}", domain="{self.domain}"'
        )
        return extended_response

    def parse_response(self, *, response: tuple[Response | None, Url]) -> dict:
        """
        Parse response object and extract needed data.
        """
        # Save Url object from response.
        url: Url = response[1]

        try:
            if response[0] is None:
                self.logger.debug(
                    f'({Probe.parse_response.__qualname__}): status="None", task_id="{self.task_id}", '
                    f'url="{url}", html="False"'
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
                # Extract html element.
                element: HtmlElement | None = self.html_extractor.page(response[0])

                # Extract favicon url.
                favicon_url: str | None = self.html_extractor.extract_favicon_url(element)
                favicon_url_obj: Url | None = self.url_extractor.parse_favicon_url(favicon_url)

                self.logger.debug(
                    f'({Probe.parse_response.__qualname__}): status="{response[0].status_code}", '
                    f'task_id="{self.task_id}", '
                    f'url="{url}", html="{True if element is not None else False}"'
                )

                prepared_response['favicon_url'] = favicon_url_obj
                return prepared_response

        except Exception as e:
            self.logger.error(
                f'({Probe.parse_response.__qualname__}): exception="{e.__class__}", message="{e}", '
                f'task_id="{self.task_id}", '
                f'url="{url}"', exc_info=True
            )
            return {
                'requested_url': url,
                'status': None,
            }

    def parse_favicon_response(self, *, response: tuple[Response | None, Url]) -> dict:
        """
        Process response received from requesting favicon url.
        Convert response content to base64 string for archiving.
        - :arg response: Returned result from calling run_request method.
        """
        # Save Url object from response.
        url: Url = response[1]
        base_response: dict = {
            'favicon_base64': None,
        }
        try:
            if response[0] is None:
                self.logger.debug(
                    f'({Probe.parse_favicon_response.__qualname__}): status="None", url="{url}", '
                    f'task_id="{self.task_id}"'
                )
                return base_response

            if response[0].is_success is True:
                # Convert response content to expected string.
                base_64_str: str = self.converter.convert_bytes_to_base64(response[0].content)
                prepared_response: dict = {
                    'favicon_base64': base_64_str,
                }

                self.logger.debug(
                    f'({Probe.parse_favicon_response.__qualname__}): status="{response[0].status_code}", '
                    f'task_id="{self.task_id}", '
                    f'url="{url}"'
                )
                return prepared_response
            else:
                return base_response

        except Exception as e:
            self.logger.error(
                f'({Probe.parse_favicon_response.__qualname__}): status="Exception", '
                f'class="{e.__class__}", message="{e}", '
                f'task_id="{self.task_id}", '
                f'url="{url}"', exc_info=True
            )
            return base_response

    @staticmethod
    def serialize_response(*, response_dict: dict) -> dict:
        """
        Serialize response in order to send it the Api.
        Convert Url objects to dictionaries.
        Ensure proper structure and types.
        - :arg response_dict: Dictionary with parsed/extracted data from responses.
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

from crawled.models.domain import Domain
from crawled.models.webpage import Webpage
from logic.adapters.base import BaseAdapter
from logic.adapters.tag import TagAdapter
from typing import Collection


class WebpageAdapter(BaseAdapter):
    """
    Adapter class for managing Webpage objects.
    """

    def __init__(self) -> None:
        self.webpage: Webpage = Webpage
        self.tag_adapter: TagAdapter = TagAdapter()
        super().__init__()

    def get_or_create_webpage_by_url(
        self,
        *,
        url: str,
        domain: Domain | None = None,
    ) -> Webpage:
        """
        Create a new Webpage object or return existing one.
        To create a new Webpage object successfully, a Domain object must be provided.
        - :arg url: String representing a Webpage url.
        - :arg domain: Parent Domain object.
        """
        try:
            existing_webpage: Webpage = self.webpage.objects.get(url=url)
            self.logger.debug(
                f'WebpageAdapter, found existing Webpage: webpage_id="{existing_webpage.id}", url="{url}"'
            )
            return existing_webpage
        except Webpage.DoesNotExist:
            assert domain is not None, 'No parent Domain provided!'
            new_webpage: Webpage = self.webpage.objects.create(parent_domain=domain, url=url)
            self.logger.debug(f'WebpageAdapter, created new Webpage: webpage_id="{new_webpage.id}", url="{url}"')
            return new_webpage

    def update_webpage(
        self,
        *,
        webpage: Webpage,
        is_homepage: bool | None = None,
        url_after_request: str | None = None,
        last_request_date: int | None = None,
        last_successful_request_date: int | None = None,
        last_http_status: str | None = None,
        last_http_status_logs: dict[int, str] | None = None,
        average_response_time: float | None = None,
        number_of_requests: int | None = None,
        number_of_successful_requests: int | None = None,
        is_active: bool | None = None,
        tags: Collection[str] | None = None,
        linking_to_webpages: Collection[str] | None = None,
        linking_to_webpages_logs: dict | None = None,
        detected_language: str | None = None,
        anchor_texts: list[str] | None = None,
        translated_anchor_texts: list[str] | None = None,
    ) -> Webpage:
        """
        Update a Webpage object.
        Updates on M2M fields are clearing the fields first!
        - :arg webpage: Webpage object to be updated.
        - :arg is_homepage: Boolean representing information whether a Webpage is a first/home page.
        - :arg url_after_request: String representing url value after requests.
            This might be different, cause of redirects.
        - :arg last_request_date: Integer representing a timestamp of last request.
        - :arg last_successful_request_date:
            Integer representing a timestamp of request with successful response code.
        - :arg last_http_status: String representing status code of last request.
        - :arg last_http_status_logs: Dictionary/Json representing a time series of http status for the Webpage.
            Where key is an Integer - representing a date/timestamp and value is a string with status code.
        - :arg average_response_time: Float representing average time to response for a Webpage.
        - :arg number_of_request: Integer representing number of total requests.
        - :arg number_of_successful_request: Integer representing number of total requests with ok status codes.
        - :arg page_rank: Float representing a rank of a Webpage.
        - :arg is_active: Boolean representing status of a Webpage.
        - :arg tags: Collection of strings representing a Tag objects.
        - :arg linking_to_webpages: Collection of string representing urls of Webpages that this page is linking to.
        - :arg linking_to_webpages_logs: Dictionary representing time series of
        """
        ...

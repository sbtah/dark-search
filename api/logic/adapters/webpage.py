from crawled.models.domain import Domain
from crawled.models.webpage import Webpage
from logic.adapters.base import BaseAdapter
from typing import Collection


class WebpageAdapter(BaseAdapter):
    """
    Adapter class for managing Webpage objects.
    """

    def __init__(self) -> None:
        self.webpage: Webpage = Webpage
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
        average_response_time: float | int | None = None,
        number_of_requests: int | None = None,
        number_of_successful_requests: int | None = None,
        is_active: bool | None = None,
        tags: Collection[str] | None = None,
        detected_language: str | None = None,
        anchor_texts: list[str] | None = None,
        translated_anchor_texts: list[str] | None = None,
    ) -> Webpage:
        ...

from datetime import date
from typing import Collection
from urllib.parse import urlsplit

from crawled.models.domain import Domain
from crawled.models.webpage import Webpage
from crawled.schemas import (
    LastHttpStatusLogsSchema,
    LinkingToWebpagesLogsSchema
)
from logic.adapters.base import BaseAdapter
from logic.adapters.domain import DomainAdapter
from logic.adapters.tag import TagAdapter


class WebpageAdapter(BaseAdapter):
    """
    Adapter class for managing Webpage objects.
    """

    def __init__(self) -> None:
        self.webpage: Webpage = Webpage
        self.tag_adapter: TagAdapter = TagAdapter()
        self.domain_adapter: Domain = DomainAdapter()
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
        if domain is None:
            value: str = urlsplit(url).netloc
            domain = self.domain_adapter.get_or_create_domain_by_value(value=value)

        try:
            existing_webpage: Webpage = self.webpage.objects.get(parent_domain=domain, url=url)
            self.logger.debug(
                f'WebpageAdapter, found existing Webpage: webpage_id="{existing_webpage.id}", url="{url}"'
            )
            return existing_webpage
        except Webpage.DoesNotExist:
            new_webpage: Webpage = self.webpage.objects.create(parent_domain=domain, url=url)
            self.logger.debug(f'WebpageAdapter, created new Webpage: webpage_id="{new_webpage.id}", url="{url}"')
            return new_webpage

    def update_webpage(
        self,
        *,
        webpage: Webpage,
        is_homepage: bool | None = None,
        url_after_request: str | None = None,
        last_request_date: date | None = None,
        last_successful_request_date: date | None = None,
        last_http_status: str | None = None,
        last_http_status_logs: dict[str, str] | None = None,
        average_response_time: float | None = None,
        number_of_requests: int | None = None,
        number_of_successful_requests: int | None = None,
        page_rank: float | None = None,
        is_active: bool | None = None,
        tags: Collection[str] | None = None,
        linking_to_webpages: Collection[str] | None = None,
        linking_to_webpages_logs: dict[str, list[int]] | None = None,
        anchor_texts: list[str] | None = None,
        translated_anchor_texts: list[str] | None = None,
    ) -> Webpage:
        """
        Update a Webpage object.
        Update is a destructive process, which means that all previous data on updated field is lost.
        - :arg webpage: Webpage object to be updated.
        - :arg is_homepage: Boolean representing information whether a Webpage is a first/home page.
        - :arg url_after_request: String representing url value after requests.
            This might be different, cause of redirects.
        - :arg last_request_date: Integer representing a timestamp of last request.
        - :arg last_successful_request_date:
            Integer representing a timestamp of request with successful response code.
        - :arg last_http_status: String representing status code of last request.
        - :arg last_http_status_logs: Dictionary/Json representing a time series of http status for the Webpage.
        - :arg average_response_time: Float representing average time to response for a Webpage.
        - :arg number_of_request: Integer representing number of total requests.
        - :arg number_of_successful_request: Integer representing number of total requests with ok status codes.
        - :arg page_rank: Float representing a rank of a Webpage.
        - :arg is_active: Boolean representing status of a Webpage.
        - :arg tags: Collection of strings representing a Tag objects.
        - :arg linking_to_webpages: Collection of string representing urls of Webpages that this page is linking to.
        - :arg linking_to_webpages_logs: Dictionary representing time series of links to webpages over time.
         - :arg anchor_texts: List of strings representing all anchor texts,
            that come with links to the Webpage.
         - :arg translated_anchor_texts: List of strings representing all anchor translated texts,
            that come with links to the Webpage.
        """
        if is_homepage is not None:
            webpage.is_homepage = is_homepage

        if url_after_request is not None:
            webpage.url_after_request = url_after_request

        if last_request_date is not None:
            webpage.last_request_date = last_request_date

        if last_successful_request_date is not None:
            webpage.last_successful_request_date = last_successful_request_date

        if last_http_status is not None:
            webpage.last_http_status = last_http_status

        if last_http_status_logs is not None:
            status_logs_model: LastHttpStatusLogsSchema = LastHttpStatusLogsSchema.model_validate(last_http_status_logs)
            webpage.last_http_status_logs = status_logs_model.model_dump()

        if average_response_time is not None:
            webpage.average_response_time = average_response_time

        if number_of_requests is not None:
            webpage.number_of_requests = number_of_requests

        if number_of_successful_requests is not None:
            webpage.number_of_successful_requests = number_of_successful_requests

        if page_rank is not None:
            webpage.page_rank = page_rank

        if is_active is not None:
            webpage.is_active = is_active

        if tags is not None:
            webpage.tags.clear()
            collection_of_tags: list = [
                self.tag_adapter.get_or_create_tag(value=tag_value) for tag_value in tags
            ]
            for found_tag in collection_of_tags:
                webpage.tags.add(found_tag)

        if linking_to_webpages is not None:
            webpage.linking_to_webpages.clear()
            collection_of_webpages: list = [
                self.get_or_create_webpage_by_url(url=found_url) for found_url in linking_to_webpages
            ]
            for found_webpage in collection_of_webpages:
                webpage.linking_to_webpages.add(found_webpage)

        if linking_to_webpages_logs is not None:
            webpages_logs_model: LinkingToWebpagesLogsSchema = LinkingToWebpagesLogsSchema.model_validate(
                linking_to_webpages_logs
            )
            webpage.linking_to_webpages_logs = webpages_logs_model.model_dump()

        if anchor_texts is not None:
            webpage.anchor_texts = anchor_texts

        if translated_anchor_texts is not None:
            webpage.translated_anchor_texts = translated_anchor_texts

        webpage.save()
        self.logger.debug(f'WebpageAdapter, updated Webpage: webpage_id="{webpage.id}"')
        return webpage

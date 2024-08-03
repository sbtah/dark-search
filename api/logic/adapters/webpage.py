from datetime import date, datetime
from typing import Collection

from crawled.models.domain import Domain
from crawled.models.webpage import Data, Webpage
from logic.schemas.url import OnPageUrlsSchema
from logic.schemas.fields import LastHttpStatusLogsSchema, LinkingToWebpagesLogsSchema
from logic.adapters.base import BaseAdapter
from logic.adapters.domain import DomainAdapter
from logic.adapters.tag import Tag, TagAdapter
from django.conf import settings


class WebpageAdapter(BaseAdapter):
    """
    Adapter class for managing Webpage objects.
    """

    def __init__(self) -> None:
        self.webpage: Webpage = Webpage
        self.data: Data = Data
        self.tag_adapter: TagAdapter = TagAdapter()
        self.domain_adapter: Domain = DomainAdapter()
        super().__init__()

    @property
    def now_date(self) -> date:
        """Return datetime object, representing current date."""
        return datetime.now()

    @property
    def now_date_str(self) -> str:
        """Return string representation of current date."""
        return self.now_date.strftime(settings.PROJECT_DATE_FORMAT)

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
        # Extract domain from webpage url.
        domain_value: str = self.domain_adapter.extract_domain(url=url)

        # Create new Domain if domain argument is None.
        if domain is None:
            domain = self.domain_adapter.get_or_create_domain_by_value(value=domain_value)

        try:
            existing_webpage: Webpage = self.webpage.objects.get(parent_domain=domain, url=url)
            self.logger.debug(
                f'WebpageAdapter, found existing Webpage: webpage_id="{existing_webpage.id}", url="{url}"'
            )
            return existing_webpage
        except Webpage.DoesNotExist:
            # Additional validation when Domain object is provided.
            assert domain.value == domain_value, f'Url {url} is not a proper child for Domain: {domain}'
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
        last_http_status_logs: dict | None = None,
        average_response_time: float | None = None,
        number_of_requests: int | None = None,
        number_of_successful_requests: int | None = None,
        page_rank: float | None = None,
        is_active: bool | None = None,
        tags: Collection[str] | None = None,
        linking_to_webpages: Collection[str] | None = None,
        linking_to_webpages_logs: dict | None = None,
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
            status_logs_model: LastHttpStatusLogsSchema = LastHttpStatusLogsSchema.model_validate(
                last_http_status_logs
            )
            validated_status_logs_data: dict = status_logs_model.model_dump()
            webpage.last_http_status_logs = validated_status_logs_data

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
            collection_of_tags: list[Tag] = [
                self.tag_adapter.get_or_create_tag(value=tag_value) for tag_value in tags
            ]
            for found_tag in collection_of_tags:
                webpage.tags.add(found_tag)

        if linking_to_webpages is not None:
            webpage.linking_to_webpages.clear()
            collection_of_webpages: list[Webpage] = [
                self.get_or_create_webpage_by_url(url=found_url) for found_url in linking_to_webpages
            ]
            for found_webpage in collection_of_webpages:
                webpage.linking_to_webpages.add(found_webpage)

        if linking_to_webpages_logs is not None:
            webpages_logs_model: LinkingToWebpagesLogsSchema = LinkingToWebpagesLogsSchema.model_validate(
                linking_to_webpages_logs
            )
            validated_webpages_logs_data: dict = webpages_logs_model.model_dump()
            webpage.linking_to_webpages_logs = validated_webpages_logs_data

        if anchor_texts is not None:
            webpage.anchor_texts = anchor_texts

        if translated_anchor_texts is not None:
            webpage.translated_anchor_texts = translated_anchor_texts

        webpage.save()
        self.logger.debug(f'WebpageAdapter, updated Webpage: webpage_id="{webpage.id}"')
        return webpage

    @staticmethod
    def process_anchor_texts(
        *,
        webpage: Webpage,
        incoming_anchor: str
    ) -> list[str] | None:
        """
        Get list of current anchor texts from Webpage object.
        Add new anchor text to existing anchors.
        Return list of strings with unique anchor texts.
        - :arg webpage: Webpage object for which anchors should be saved.
        - :arg incoming_anchor: String representing newly found anchor text to be added.
        """
        if len(incoming_anchor) == 0:
            return None
        current_anchors: list[str] = webpage.anchor_texts
        # Add new anchor text.
        # To ensure that each item is unique we are casting list to set.
        anchors_set: set = set(current_anchors)
        anchors_set.add(incoming_anchor)
        return list(anchors_set)

    @staticmethod
    def process_number_of_requests(
        *,
        webpage: Webpage,
    ) -> int:
        """
        Calculate new number_of_requests for Webpage object.
        - :arg number_of_requests: Number of requests for current url in 'requested_url'.
        """
        current_number_of_requests: int = webpage.number_of_requests
        new_number_of_requests: int = current_number_of_requests + 1
        return new_number_of_requests

    @staticmethod
    def process_number_of_successful_requests(
        *,
        webpage: Webpage,
        status: str | None,
    ) -> int | None:
        """
        Calculate new `number_of_successful_requests` for current Webpage object.
        - :arg webpage: Webpage object for which calculation should happen.
        - :arg status: String representing Http status from response.
        """
        current_number_of_successful_requests: int = webpage.number_of_successful_requests

        if status is None:
            return None

        if status is not None and status[0] not in {'2', '3'}:
            return None

        if status is not None and status[0] in {'2', '3'}:
            new_number_of_successful_requests: int = current_number_of_successful_requests + 1
            return new_number_of_successful_requests

    @staticmethod
    def process_average_response_time(
        *,
        webpage: Webpage,
        response_time: int,
    ) -> float:
        """
        Calculate `average_response_time` for given Webpage object.
        - :arg webpage: Webpage object for which calculation should happen.
        - :arg response_time: Response time for Webpage.
        """
        current_average_response: float = webpage.average_response_time

        if current_average_response == 0:
            return float(response_time)

        current_number_of_requests: int = webpage.number_of_requests
        new_average: float = float((current_average_response + response_time) / current_number_of_requests)
        return new_average

    @staticmethod
    def process_last_http_status_logs(
        *,
        webpage: Webpage,
        status: str,
        current_date_str: str,
    ) -> dict | None:
        """
        Process Http status from last response.
        Create a log from last Http response status.
        Return an updated version of logs for a `last_http_status_logs`.
        - :arg webpage: Webpage object that is currently being processed.
        - :arg status: Http status from response.
        - :arg current_date_str: String representing current date in desired format.
        """
        current_webpage_status_logs: dict = webpage.last_http_status_logs
        logs_dates: set[str] = set([d['date'] for d in current_webpage_status_logs['status_logs']])

        if current_date_str in logs_dates:
            return None

        new_log: dict = {'date': current_date_str, 'status': status}
        updated_logs: dict = current_webpage_status_logs['status_logs'].append(new_log)
        return updated_logs

    def create_data_for_webpage(
        self,
        *,
        webpage: Webpage,
        page_title: str | None = None,
        meta_title: str | None = None,
        meta_description: str | None = None,
        content_type: str | None = None,
        raw_text: str | None = None,
        on_page_raw_urls: dict | None = None,
        on_page_processed_internal_urls: dict | None = None,
        on_page_processed_external_urls: dict | None = None,
    ) -> Data:
        """
        Create a Data object for a given Webpage.
        Raise AssertionError if the Webpage already has a Data object.
        - :arg webpage: Webpage object for which the Data object should be created or updated.
        - :arg page_title: String with extracted page title (h1).
        - :arg meta_title: String with extracted text from meta title.
        - :arg meta_description: String with extracted text from meta description.
        - :arg raw_text: String with extracted text content from a Webpage.
        - :arg on_page_raw_urls: Dictionary with list of all urls found on a Webpage.
        - :arg on_page_processed_internal_urls:
            Dictionary with a list of processed urls that are within the parent Domain of the current Webpage.
        - :arg on_page_processed_external_urls:
            Dictionary with a list of processed urls that leads outside the parent Domain of the current Webpage.
        """
        assert webpage.has_data is False, 'The given Webpage object already has a defined Data.'
        creation_data = {
            'webpage': webpage,
        }
        if page_title is not None:
            creation_data['page_title'] = page_title

        if meta_title is not None:
            creation_data['meta_title'] = meta_title

        if meta_description is not None:
            creation_data['meta_description'] = meta_description

        if content_type is not None:
            creation_data['content_type'] = content_type

        if raw_text is not None:
            creation_data['raw_text'] = raw_text

        if on_page_raw_urls is not None:
            on_page_raw_urls_model = OnPageUrlsSchema.model_validate(on_page_raw_urls)
            on_page_raw_urls: dict = on_page_raw_urls_model.model_dump()
            creation_data['on_page_raw_urls'] = on_page_raw_urls

        if on_page_processed_internal_urls is not None:
            on_page_processed_internal_model: OnPageUrlsSchema = OnPageUrlsSchema.model_validate(
                on_page_processed_internal_urls
            )
            on_page_processed_internal_urls: dict = on_page_processed_internal_model.model_dump()
            creation_data['on_page_processed_internal_urls'] = on_page_processed_internal_urls

        if on_page_processed_external_urls is not None:
            on_page_processed_external_model: OnPageUrlsSchema = OnPageUrlsSchema.model_validate(
                on_page_processed_external_urls
            )
            on_page_processed_external_urls: dict = on_page_processed_external_model.model_dump()
            creation_data['on_page_processed_external_urls'] = on_page_processed_external_urls

        data: Data = self.data.objects.create(**creation_data)
        self.logger.debug(f'WebpageAdapter, created new Data: data_id="{data.id}"')
        return data

    def update_data_for_webpage(
        self,
        *,
        webpage: Webpage,
        page_title: str | None = None,
        meta_title: str | None = None,
        meta_description: str | None = None,
        content_type: str | None = None,
        raw_text: str | None = None,
        on_page_raw_urls: dict | None = None,
        on_page_processed_internal_urls: dict | None = None,
        on_page_processed_external_urls: dict | None = None,
        detected_languages: list[str] | None = None,
        translated_text: str | None = None,
    ):
        """
        Update a Data object for a given Webpage.
        Raise AssertionError if the Webpage ha no Data defined.
        - :arg webpage: Webpage object for which the Data object should be created or updated.
        - :arg page_title: String with extracted page title (h1).
        - :arg meta_title: String with extracted text from meta title.
        - :arg meta_description: String with extracted text from meta description.
        - :arg raw_text: String with extracted text content from a Webpage.
        - :arg on_page_raw_urls: Dictionary with list of all urls found on a Webpage.
        - :arg on_page_processed_internal_urls:
            Dictionary with a list of processed urls that are within the parent Domain of the current Webpage.
        - :arg on_page_processed_external_urls:
            Dictionary with a list of processed urls that leads outside the parent Domain of the current Webpage.
        - :arg detected_languages: List of detected languages on page.
        - :arg translated_text: String with translated text from raw_text.
        """
        assert webpage.has_data is True, 'The give Webpage object has no defined Data.'

        # Get Data object for given Webpage.
        data: Data = webpage.data

        if page_title is not None:
            data.page_title = page_title

        if meta_title is not None:
            data.meta_title = meta_title

        if meta_description is not None:
            data.meta_description = meta_description

        if content_type is not None:
            data.content_type = content_type

        if raw_text is not None:
            data.raw_text = raw_text

        if on_page_raw_urls is not None:
            on_page_raw_urls_model: OnPageUrlsSchema = OnPageUrlsSchema.model_validate(
                on_page_raw_urls
            )
            on_page_raw_urls: dict = on_page_raw_urls_model.model_dump()
            data.on_page_raw_urls = on_page_raw_urls

        if on_page_processed_internal_urls is not None:
            on_page_processed_internal_model: OnPageUrlsSchema = OnPageUrlsSchema.model_validate(
                on_page_processed_internal_urls
            )
            on_page_processed_internal_urls: dict = on_page_processed_internal_model.model_dump()
            data.on_page_processed_internal_urls = on_page_processed_internal_urls

        if on_page_processed_external_urls is not None:
            on_page_processed_external_model: OnPageUrlsSchema = OnPageUrlsSchema.model_validate(
                on_page_processed_external_urls
            )
            on_page_processed_external_urls: dict = on_page_processed_external_model.model_dump()
            data.on_page_processed_external_urls = on_page_processed_external_urls

        if detected_languages is not None:
            data.detected_languages = detected_languages

        if translated_text is not None:
            data.translated_text = translated_text

        data.save()
        self.logger.debug(f'WebpageAdapter, updated Data: data_id="{data.id}"')
        return data

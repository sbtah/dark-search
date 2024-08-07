"""
Test cases for Webpage Adapter class.
"""
from datetime import datetime, date
from unittest.mock import MagicMock

import pytest
from crawled.models.webpage import Data, Webpage
from django.conf import settings
from logic.adapters.webpage import WebpageAdapter
from pydantic import ValidationError


pytestmark = pytest.mark.django_db


@pytest.fixture
def adapter() -> WebpageAdapter:
    """
    Fixture returning instance of WebpageAdapter.
    Logging is turned off in testing.
    """
    adapter: WebpageAdapter = WebpageAdapter()
    adapter.logger = MagicMock()
    return adapter


class TestWebpageAdapter:
    """Test cases for WebpageAdapter functionality."""

    def test_webpage_adapter_now_date_returns_date_object(self, adapter) -> None:
        """
        Test that `now_date` property is returning datetime object.
        """
        return_value = adapter.now_date
        assert isinstance(return_value, date)

    def test_webpage_adapter_now_date_str_returns_date_in_desired_format(
        self,
        adapter,
    ) -> None:
        """
        Test that `now_date_str` property is returning string representing date in desired format.
        """
        return_value = adapter.now_date_str
        assert isinstance(return_value, str)

    def test_webpage_adapter_get_or_create_webpage_by_url_return_existing_webpage(
        self,
        adapter,
        example_webpage,
    ) -> None:
        """
        Test that get_or_create_webpage_by_url
        is successfully returning an existing Webpage object.
        """
        return_value = adapter.get_or_create_webpage_by_url(url='http://test.com')
        assert isinstance(return_value, Webpage)
        assert return_value.url == 'http://test.com'

    def test_webpage_adapter_get_or_create_webpage_by_url_create_new_object(
        self,
        adapter,
        example_domain,
    ) -> None:
        """
        Test that get_or_create_webpage_by_url is successfully creating a new Webpage object.
        """
        return_value = adapter.get_or_create_webpage_by_url(
            domain=example_domain, url='http://test.com'
        )
        assert isinstance(return_value, Webpage)
        assert return_value.url == 'http://test.com'
        assert return_value.parent_domain == example_domain

    def test_webpage_adapter_get_or_create_webpage_by_url_is_raisin_assertion_error(
        self,
        adapter,
        example_domain,
    ) -> None:
        """
        Test that get_or_create_webpage_by_url is raising assertion error,
        while trying to create a Webpage with different domain if provided parent domain.
        """
        with pytest.raises(AssertionError):
            adapter.get_or_create_webpage_by_url(domain=example_domain, url='http://other.com/page-1')

    def test_webpage_adapter_update_webpage_is_successful(
        self,
        adapter,
        example_webpage,
        collection_of_tags,
        collection_of_webpages_urls,
    ) -> None:
        """
        Test that update_webpage is properly updating fields on the provided Webpage object.
        """
        crawl_date = datetime.now()
        log_data = crawl_date.strftime(settings.PROJECT_DATE_FORMAT)

        status_logs_data = {
            'status_logs': [
                {'date': log_data, 'status': '200'},
                {'date': log_data, 'status': '200'}
            ]
        }
        webpages_logs_data = {
            'webpages_logs': [
                {'date': '20-11-2021 07:11', 'urls': ['https://test.onion.page1', 'http://test.onion/page-2']},
                {'date': '20-11-2021 05:22', 'urls': ['https://test.onion.page1', ]}
            ]
        }
        return_value = adapter.update_webpage(
            webpage=example_webpage,
            is_homepage=True,
            url_after_request='http://redirected.onion/page-1',
            last_request_date=crawl_date,
            last_successful_request_date=crawl_date,
            last_http_status='200',
            last_http_status_logs=status_logs_data,
            average_response_time=1.25,
            number_of_requests=10,
            number_of_successful_requests=10,
            page_rank=7.77,
            is_active=True,
            tags=collection_of_tags,
            linking_to_webpages=collection_of_webpages_urls,
            linking_to_webpages_logs=webpages_logs_data,
            anchor_texts=['BULLSHIT', 'LOLS', 'GUNS'],
            translated_anchor_texts=['BULLSHIT', 'LOLS', 'GUNS'],
        )
        assert isinstance(return_value, Webpage)
        assert example_webpage.is_homepage is True
        assert example_webpage.url_after_request == 'http://redirected.onion/page-1'
        assert example_webpage.last_request_date == crawl_date
        assert example_webpage.last_successful_request_date == crawl_date
        assert example_webpage.last_http_status == '200'
        assert example_webpage.last_http_status_logs == status_logs_data
        assert example_webpage.average_response_time == 1.25
        assert example_webpage.number_of_requests == 10
        assert example_webpage.number_of_successful_requests == 10
        assert example_webpage.page_rank == 7.77
        assert example_webpage.is_active is True
        assert example_webpage.tags.count() == 5
        assert example_webpage.linking_to_webpages.count() == 5
        assert example_webpage.linking_to_webpages_logs == webpages_logs_data
        assert example_webpage.anchor_texts == ['BULLSHIT', 'LOLS', 'GUNS']
        assert example_webpage.translated_anchor_texts == ['BULLSHIT', 'LOLS', 'GUNS']

    def test_webpage_adapter_update_webpage_is_raising_exception_for_http_status_logs(
        self,
        adapter,
        example_webpage,
        collection_of_tags,
        collection_of_webpages_urls,
    ) -> None:
        """
        Test that update_webpage is properly validating and raising exception if data for
        'last_http_status_logs' is not matching a provided Schema.
        """
        crawl_date = datetime.now()
        log_data = crawl_date.strftime(settings.PROJECT_DATE_FORMAT)

        bad_data = {
            'status_logs': [
                {'date': log_data, 'status': 200},
                {'date': '2024', 'status': '200'}
            ]
        }
        webpages_logs_data = {
            'webpages_logs': [
                {'date': '20-11-2021 07:11', 'urls': ['https://test.onion.page1', 'http://test.onion/page-2']},
                {'date': '20-11-2021 05:22', 'urls': ['https://test.onion.page1',]}
            ]
        }
        with pytest.raises(ValidationError):
            adapter.update_webpage(
                webpage=example_webpage,
                is_homepage=True,
                url_after_request='http://redirected.onion/page-1',
                last_request_date=crawl_date,
                last_successful_request_date=crawl_date,
                last_http_status='200',
                last_http_status_logs=bad_data,
                average_response_time=1.25,
                number_of_requests=10,
                number_of_successful_requests=10,
                page_rank=7.77,
                is_active=True,
                tags=collection_of_tags,
                linking_to_webpages=collection_of_webpages_urls,
                linking_to_webpages_logs=webpages_logs_data,
                anchor_texts=['BULLSHIT', 'LOLS', 'GUNS'],
                translated_anchor_texts=['BULLSHIT', 'LOLS', 'GUNS'],
            )

    def test_webpage_adapter_update_webpage_is_raising_exception_for_linking_webpages_logs(
        self,
        adapter,
        example_webpage,
        collection_of_tags,
        collection_of_webpages_urls,
    ) -> None:
        """
        Test that update_webpage is properly validating and raising exception if data for
        'linking_to_webpages_logs' is not matching a provided Schema.
        """
        crawl_date = datetime.now()
        log_data = crawl_date.strftime(settings.PROJECT_DATE_FORMAT)

        status_logs_data = {
            'status_logs': [
                {'date': log_data, 'status': '200'},
                {'date': log_data, 'status': '200'}
            ]
        }
        bad_data = {
            'webpages_logs': [
                {'date': '20-11-2021', 'urls': ['https://test.onion.page1', 'http://test.onion/page-2']},
                {'date': '20-11-2021 05:22', 'urls': ['https://test.onion.page1',]}
            ]
        }
        with pytest.raises(ValidationError):
            adapter.update_webpage(
                webpage=example_webpage,
                is_homepage=True,
                url_after_request='http://redirected.onion/page-1',
                last_request_date=crawl_date,
                last_successful_request_date=crawl_date,
                last_http_status='200',
                last_http_status_logs=status_logs_data,
                average_response_time=1.25,
                number_of_requests=10,
                number_of_successful_requests=10,
                page_rank=7.77,
                is_active=True,
                tags=collection_of_tags,
                linking_to_webpages=collection_of_webpages_urls,
                linking_to_webpages_logs=bad_data,
                anchor_texts=['BULLSHIT', 'LOLS', 'GUNS'],
                translated_anchor_texts=['BULLSHIT', 'LOLS', 'GUNS'],
            )

    def test_webpage_adapter_create_data_for_webpage_is_successful(
        self,
        adapter,
        example_webpage,
    ) -> None:
        """
        Test that create_data_for_webpage method is successfully creating Data object.
        """
        assert Data.objects.count() == 0
        json_on_page_urls: dict = {
            'on_page_urls': [{'value': 'http://test.onion/page-1', 'anchor': 'Site'}]
        }
        result_value = adapter.create_data_for_webpage(
            webpage=example_webpage,
            page_title='Some test title',
            meta_title='Some meta title',
            meta_description='Webpage description',
            content_type='text/html; charset=UTF-8',
            raw_text='TEXT FROM THE ACTUAL WEBPAGE!',
            on_page_raw_urls=json_on_page_urls,
            on_page_processed_internal_urls=json_on_page_urls,
            on_page_processed_external_urls=json_on_page_urls,
        )
        assert isinstance(result_value, Data)
        assert Data.objects.count() == 1

    def test_webpage_adapter_create_data_for_webpage_is_raising_validation_error_for_json_fields(
        self,
        adapter,
        example_webpage,
    ) -> None:
        """
        Test that create_data_for_webpage method is raising ValidationError
        when data for JsonFields does not match schema.
        """
        json_on_page_urls_bad: dict = {
            'on_page_urls': [{'href': 'http://test.onion/page-1', 'text': 1}]
        }
        with pytest.raises(ValidationError):
            adapter.create_data_for_webpage(
                webpage=example_webpage,
                page_title='Some test title',
                meta_title='Some meta title',
                meta_description='Webpage description',
                raw_text='TEXT FROM THE ACTUAL WEBPAGE!',
                on_page_raw_urls=json_on_page_urls_bad,
                on_page_processed_internal_urls=json_on_page_urls_bad,
                on_page_processed_external_urls=json_on_page_urls_bad,
            )

    def test_webpage_adapter_create_data_for_webpage_is_raising_assertion_error(
        self,
        adapter,
        example_webpage_with_data
    ) -> None:
        """
        Test that create_data_for_webpage is raising AssertionError,
        for Webpage with existing Data.
        """
        with pytest.raises(AssertionError):
            adapter.create_data_for_webpage(webpage=example_webpage_with_data)

    def test_webpage_adapter_update_data_for_webpage_is_successful(
        self,
        adapter,
        example_webpage_with_data,
    ) -> None:
        """
        Test that update_data_for_webpage is successfully updating Data object.
        """
        json_on_page_urls: dict = {
            'on_page_urls': [{'value': 'http://test.onion/page-1', 'anchor': 'Site'}]
        }
        return_value = adapter.update_data_for_webpage(
            webpage=example_webpage_with_data,
            page_title='Test title',
            meta_title='Meta title',
            meta_description='Test description',
            content_type='text/html; charset=UTF-8',
            raw_text='Some text',
            on_page_raw_urls=json_on_page_urls,
            on_page_processed_internal_urls=json_on_page_urls,
            on_page_processed_external_urls=json_on_page_urls,
            detected_languages=['German'],
            translated_text='Some text',
        )
        assert isinstance(return_value, Data)
        assert return_value.page_title == 'Test title'
        assert return_value.meta_title == 'Meta title'
        assert return_value.meta_description == 'Test description'
        assert return_value.content_type == 'text/html; charset=UTF-8'
        assert return_value.raw_text == 'Some text'
        assert return_value.on_page_raw_urls == json_on_page_urls
        assert return_value.on_page_processed_internal_urls == json_on_page_urls
        assert return_value.on_page_processed_external_urls == json_on_page_urls
        assert return_value.detected_languages == ['German']
        assert return_value.translated_text == 'Some text'

    def test_webpage_adapter_update_data_for_webpage_is_raising_assertion_error(
        self,
        adapter,
        example_webpage,
    ) -> None:
        """
        Test that update_data_for_webpage is raising AssertionError,
        for Webpage with no Data.
        """
        with pytest.raises(AssertionError):
            adapter.update_data_for_webpage(webpage=example_webpage)

    def test_webpage_adapter_update_data_for_webpage_is_raising_validation_error_for_json_fields(
        self,
        adapter,
        example_webpage_with_data,
    ) -> None:
        """
        Test that update_data_for_webpage method is raising ValidationError
        when data for JsonFields does not match schema.
        """
        json_on_page_urls_bad: dict = {
            'on_page_urls': [{'href': 'http://test.onion/page-1', 'text': 1}]
        }
        with pytest.raises(ValidationError):
            adapter.update_data_for_webpage(
                webpage=example_webpage_with_data,
                page_title='Some test title',
                meta_title='Some meta title',
                meta_description='Webpage description',
                content_type='text/html; charset=UTF-8',
                raw_text='TEXT FROM THE ACTUAL WEBPAGE!',
                on_page_raw_urls=json_on_page_urls_bad,
                on_page_processed_internal_urls=json_on_page_urls_bad,
                on_page_processed_external_urls=json_on_page_urls_bad,
            )

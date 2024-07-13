"""
Test cases for HtmlExtractor functionality.
"""
from unittest.mock import MagicMock

import pytest
from httpx import Response
from logic.parsers.html import HtmlExtractor
from lxml.html import HtmlElement


class TestHtmlExtractor:
    """Test cases for HtmlExtractor class."""

    def test_html_extractor_page_returns_html_element(self):
        """Test that page method is returning HtmlElement object."""
        fake_response = MagicMock(
            spec=Response, text='<html><head></head><body><p>Test</p></body></html>'
        )
        element = HtmlExtractor().page(response=fake_response)
        assert isinstance(element, HtmlElement)

    def test_html_extractor_page_raises_exception_for_empty_text(self):
        """Test that page method is not raising an Exception and returns None."""
        fake_response = MagicMock(spec=Response, text='')
        element = HtmlExtractor().page(response=fake_response)
        assert element is None

    def test_html_extractor_extract_urls_with_texts_returns_list_of_dictionaries(self, many_urls_element):
        """Test that extract_urls_with_text method is returning expected number of dictionaries."""
        urls = HtmlExtractor().extract_urls_with_texts(many_urls_element)
        assert isinstance(urls, list)
        assert len(urls) == 2
        assert isinstance(urls[0], dict)
        assert isinstance(urls[1], dict)
        assert isinstance(urls[0]['url'], str)
        assert isinstance(urls[1]['url'], str)
        assert isinstance(urls[0]['anchor'], str)
        assert isinstance(urls[1]['anchor'], str)

    def test_html_extractor_extract_urls_with_texts_is_not_returning_empty_strings(self, empty_urls_element):
        """Test that extract_urls_with_texts is returning expected number of urls."""
        urls = HtmlExtractor().extract_urls_with_texts(empty_urls_element)
        assert isinstance(urls, list)
        assert len(urls) == 1

    def test_html_extractor_extract_urls_with_texts_returns_empty_strings_for_elements_without_anchor(
        self, empty_texts_urls_element
    ):
        """Test that extract_urls_with_texts is returning expected number of urls."""
        urls = HtmlExtractor().extract_urls_with_texts(empty_texts_urls_element)
        assert isinstance(urls, list)
        assert len(urls) == 2
        assert isinstance(urls[0]['anchor'], str)
        assert urls[0]['anchor'] == ''
        assert isinstance(urls[1]['anchor'], str)
        assert urls[1]['anchor'] == ''

    def test_html_extractor_extract_urls_with_text_returns_none(self, no_urls_element):
        """Test that extract_urls method is returning None if no urls were found in the element."""
        urls = HtmlExtractor().extract_urls_with_texts(no_urls_element)
        assert urls is None

    def test_html_extractor_extract_favicon_url_returns_string_with_url(self, favicon_url_element):
        """Test that extract_favicon_url method is returning string with favicon url."""
        favicon_url = HtmlExtractor().extract_favicon_url(favicon_url_element)
        assert isinstance(favicon_url, str)
        assert favicon_url == '/favicon.ico'

    def test_html_extractor_extract_favicon_url_returns_none(self, no_urls_element):
        """Test that extract_favicon_url method is returning None if no favicon url was found."""
        favicon_url = HtmlExtractor().extract_favicon_url(no_urls_element)
        assert favicon_url is None

    def test_html_extractor_extract_page_title_returns_string_with_url(self, nested_h1_element):
        """Test that extract_page_title method is returning string with h1 tag text content."""
        page_title = HtmlExtractor().extract_page_title(nested_h1_element)
        assert isinstance(page_title, str)
        assert page_title == 'This is a title'

    def test_html_extractor_extract_page_title_returns_none(self, no_urls_element):
        """Test that extract_page_title returns None if no h1 tags were found."""
        page_title = HtmlExtractor().extract_page_title(no_urls_element)
        assert page_title is None

    def test_html_extractor_extract_meta_title_returns_string(self, meta_title_element):
        """Test that extract_meta_title returns meta title on success."""
        meta_title = HtmlExtractor().extract_meta_title(meta_title_element)
        assert isinstance(meta_title, str)
        assert meta_title == 'Test Page'

    def test_html_extractor_extract_meta_title_returns_none(self, no_urls_element):
        """Test that extract_meta_title returns None if no title tag was found."""
        meta_title = HtmlExtractor().extract_meta_title(no_urls_element)
        assert meta_title is None

    def test_html_extractor_extract_meta_description_returns_string(self, meta_description_element):
        """Test that extract_meta_description is returning meta description text content on success."""
        meta_description = HtmlExtractor().extract_meta_description(meta_description_element)
        assert isinstance(meta_description, str)
        assert meta_description == 'Description!'

    def test_html_extractor_extract_entire_text_returns_desired_string(self, example_webpage_element):
        """Test that extract_entire_text is returning string with proper content."""
        content = HtmlExtractor().extract_entire_text(example_webpage_element)
        assert isinstance(content, str)
        assert content == 'This is a titleTestLink 1Link 1'

    def test_html_extractor_extract_entire_text_returns_none_on_exception(self, mocker, no_urls_element):
        """Test that extract_html_body is returning an empty string on any Exception."""
        mocked = mocker.patch('logic.parsers.html.HtmlExtractor.extract_entire_text', side_effect=Exception)
        assert mocked.assert_called_once
        with pytest.raises(Exception):
            text = HtmlExtractor().extract_entire_text(no_urls_element)
            assert text is None

    def test_html_extractor_parse_is_successful(self, example_webpage_element):
        """Test that parse method is returning dictionary with extracted data."""
        parse_data = HtmlExtractor().parse(example_webpage_element)
        assert isinstance(parse_data, dict)
        assert isinstance(parse_data['text'], str)
        assert isinstance(parse_data['page_title'], str)
        assert parse_data['page_title'] == 'This is a title'
        assert isinstance(parse_data['meta_title'], str)
        assert parse_data['meta_title'] == 'Test Page'
        assert isinstance(parse_data['meta_description'], str)
        assert parse_data['meta_description'] == 'Description!'
        assert isinstance(parse_data['on_page_urls'], list)
        assert len(parse_data['on_page_urls']) == 2
        assert isinstance(parse_data['favicon_url'], str)
        assert parse_data['favicon_url'] == '/favicon.ico'

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
        """Test that page method is not raising a ParserError exception"""
        fake_response = MagicMock(spec=Response, text='')
        element = HtmlExtractor().page(response=fake_response)
        assert element is None

    def test_html_extractor_extract_urls_returns_list_of_urls(self, many_urls_element):
        """Test that extract_urls method is returning expected number or urls"""
        urls = HtmlExtractor().extract_urls(many_urls_element)
        assert isinstance(urls, list)
        assert len(urls) == 2

    def test_html_extractor_extract_urls_is_not_returning_empty_strings(self, empty_urls_element):
        """Test that extract_urls method is returning expected number or urls"""
        urls = HtmlExtractor().extract_urls(empty_urls_element)
        assert isinstance(urls, list)
        assert len(urls) == 1

    def test_html_extractor_extract_urls_is_returns_none(self, no_urls_element):
        """Test that extract_urls method is returning None if no urls were found in the element."""
        urls = HtmlExtractor().extract_urls(no_urls_element)
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
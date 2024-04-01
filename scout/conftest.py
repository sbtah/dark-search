"""
Pytest fixtures
"""
import pytest
from logic.parsers.url import UrlExtractor


@pytest.fixture
def url_extractor():
    starting_url = 'http://example.onion'
    urls_collection = [
        'http://example.onion/page', 'http://example.onion/path?page=1', 'http://external.onion/',
        'page.html', '/path', 'ftp://example.onion/baz'
    ]
    return UrlExtractor(starting_url, urls_collection)

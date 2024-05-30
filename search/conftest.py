"""
Pytest fixtures
"""
import pytest
from logic.parsers.url import UrlExtractor
from parameters.models import Proxy, UserAgent
from lxml.html import fromstring


@pytest.fixture
def url_extractor():
    starting_url = 'http://example.onion'
    return UrlExtractor(starting_url)


@pytest.fixture
def urls_collection():
    urls_collection = [
        'http://example.onion/page', 'http://example.onion/path?page=1', 'http://external.onion/',
        'page.html', '/path', 'ftp://example.onion/baz'
    ]
    return urls_collection


@pytest.fixture
def user_agent():
    return UserAgent.objects.create(value='Mozilla/5.0 Test Agent')


@pytest.fixture
def many_agents():
    for _ in range (1, 11):
        UserAgent.objects.create(value=f'Mozilla/5.0 Test Agent {_}')


@pytest.fixture
def many_proxies():
    for _ in range(1, 11):
        Proxy.objects.create(value=f'127.0.0.{_}', current_spiders=_)


@pytest.fixture
def many_urls_element():
    return fromstring(
        '<html><head></head><body><p>Test</p><a href="http://test-url-1.com">Link 1<a/><a href="http://test-url-2.com">Link 1<a/></body></html>'
    )


@pytest.fixture
def empty_urls_element():
    return fromstring(
        '<html><head></head><body><p>Test</p><a href="http://test-url-1.com">Link 1<a/><a href="">Link 1<a/></body></html>'
    )


@pytest.fixture
def no_urls_element():
    return fromstring(
        '<html><head></head><body><p>Test</p></body></html>'
    )


@pytest.fixture
def favicon_url_element():
    return fromstring(
        '<html><head><link href="/favicon.ico"></head><body><p>Test</p></body></html>'
    )


@pytest.fixture
def nested_h1_element():
    return fromstring(
        '<html><head></head><body><h1><div><p>This is a title</p></div></h1></body></html>'
    )

@pytest.fixture
def meta_title_element():
    return fromstring(
        '<html><head><title>Test Page</title></head><body><p>Test</p></body></html>'
    )

@pytest.fixture
def meta_description_element():
    return fromstring(
        '<html><head><meta name="description" content="Description!"></head><body><p>Test</p></body></html>'
    )


@pytest.fixture
def example_webpage_element():
    return fromstring(
        """
        <html>
            <head>
                <title>Test Page</title><link href="/favicon.ico"><meta name="description" content="Description!">
            </head>
            <body>
                <h1><div><p>This is a title</p></div></h1>
                <p>Test</p><a href="http://test-url-1.com">Link 1<a/><a href="http://test-url-2.com">Link 1<a/>
            </body>
        </html>
        """
    )

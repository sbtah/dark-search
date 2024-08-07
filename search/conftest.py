"""
Pytest fixtures
"""
import pytest
from logic.adapters.url import UrlAdapter
from search.logic.objects.url import Url
from logic.parsers.url import UrlExtractor
from lxml.html import HtmlElement, fromstring
from parameters.models import Proxy, UserAgent


@pytest.fixture
def url_extractor() -> UrlExtractor:
    starting_url = UrlAdapter.create_url_object(value='http://example.onion')
    return UrlExtractor(starting_url)


@pytest.fixture
def urls_collection() -> list[dict[str, str]]:
    urls_collection = [
        {'value': 'http://example.onion/page', 'anchor': 'Url 1'},
        {'value': 'http://example.onion/path?page=1', 'anchor': 'Url 2'},
        {
            'value': 'http://example.onion/path?query=string#fragment',
            'anchor': 'Url 3'
        },
        {'value': '/page.php?q=canary', 'anchor': 'Canary'},
        {'value': '/page.php?q=main&l=it', 'anchor': 'Italiano'},
        {'value': '/page.php?q=shell', 'anchor': 'Shell Accounts'},
        {'value': 'http://example.onion/path#fragment', 'anchor': 'Url 4'},
        {'value': 'http://other.onion', 'anchor': 'Url 5'},
        {'value': 'http://external.onion', 'anchor': ''},
        {'value': 'page.html', 'anchor': '...'},
        {'value': 'page.php', 'anchor': '....'},
        {'value': '/file.txt', 'anchor': 'page.php.'},
        {'value': '/path', 'anchor': 'Test text'},
        {'value': 'ftp://example.onion/baz', 'anchor': ''},
        {'value': 'http://example.onion/some.jpeg', 'anchor': 'Image 1'},
        {'value': 'some-2.jpeg', 'anchor': 'Image 2'},
        {'value': '/some-3.jpeg', 'anchor': 'Image 3'},
        {'value': 'http://example.onion/some.pdf', 'anchor': 'Pdf 1'},
        {'value': 'example.onion', 'anchor': 'malformed url'},
        {'value': 'external-2.onion', 'anchor': 'malformed url 2'}
    ]
    return urls_collection


@pytest.fixture
def user_agent() -> UserAgent:
    return UserAgent.objects.create(value='Mozilla/5.0 Test Agent')


@pytest.fixture
def many_agents() -> None:
    for _ in range(1, 11):
        UserAgent.objects.create(value=f'Mozilla/5.0 Test Agent {_}')


@pytest.fixture
def many_proxies() -> None:
    for _ in range(1, 11):
        Proxy.objects.create(value=f'127.0.0.{_}', current_spiders=_)


@pytest.fixture
def many_urls_element() -> HtmlElement:
    return fromstring(
        '<html>'
        '<head></head>'
        '<body>'
        '<p>Test</p>'
        '<a href="http://test-url-1.com">Link 1<a/>'
        '<a href="http://test-url-2.com">Link 2<a/>'
        '</body>'
        '</html>'
    )


@pytest.fixture
def empty_urls_element() -> HtmlElement:
    return fromstring(
        '<html>'
        '<head></head>'
        '<body>'
        '<p>Test</p>'
        '<a href="http://test-url-1.com">Link 1<a/><a href="">Link 1<a/>'
        '</body>'
        '</html>'
    )


@pytest.fixture
def empty_texts_urls_element() -> HtmlElement:
    return fromstring(
        '<html>'
        '<head></head>'
        '<body>'
        '<p>Test</p>'
        '<a href="http://test-url-1.com"><a/>'
        '<a href="http://test-url-2.com"><a/>'
        '</body>'
        '</html>'
    )


@pytest.fixture
def no_urls_element() -> HtmlElement:
    return fromstring(
        '<html><head></head><body><p>Test</p></body></html>'
    )


@pytest.fixture
def favicon_url_element() -> HtmlElement:
    return fromstring(
        '<html>'
        '<head><link href="/favicon.ico"></head><body><p>Test</p></body>'
        '</html>'
    )


@pytest.fixture
def nested_h1_element() -> HtmlElement:
    return fromstring(
        '<html>'
        '<head></head>'
        '<body><h1><div><p>This is a title</p></div></h1></body>'
        '</html>'
    )


@pytest.fixture
def meta_title_element() -> HtmlElement:
    return fromstring(
        '<html>'
        '<head><title>Test Page</title></head><body><p>Test</p></body>'
        '</html>'
    )


@pytest.fixture
def meta_description_element() -> HtmlElement:
    return fromstring(
        '<html>'
        '<head><meta name="description" content="Description!"></head>'
        '<body><p>Test</p></body>'
        '</html>'
    )


@pytest.fixture
def example_webpage_element() -> HtmlElement:
    return fromstring(
        '<html>'
        '<head>'
        '<title>Test Page</title><link href="/favicon.ico"><meta name="description" content="Description!">'
        '</head>'
        '<body>'
        '<h1><div><p>This is a title</p></div></h1>'
        '<p>Test</p><a href="http://test-url-1.com">Link 1<a/>'
        '<a href="http://test-url-2.com">Link 1<a/>'
        '</body>'
        '</html>'
    )


@pytest.fixture
def example_text_response() -> str:
    text = """
        <html>
        <head>
        <title>Test Page</title>
        <link href="/favicon.ico">
        <meta name="description" content="Description!">
        </head>
        <body>
        <h1><div><p>This is a title</p></div></h1>
        <p>Test</p><a href="http://test-url-1.com">Link 1<a/>
        <a href="http://test-url-2.com">Link 1<a/>
        </body>
        </html>
        """
    return text


@pytest.fixture
def example_url_object() -> Url:
    url = Url(value='http://found.onion/')
    return url


@pytest.fixture
def example_url_objects() -> list[Url]:
    """Collection of Url objects."""
    urls = [Url(value=f'http://found.onion/page{_}') for _ in range(5)]
    return urls

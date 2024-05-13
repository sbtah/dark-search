"""
Pytest fixtures
"""
import pytest
from logic.parsers.url import UrlExtractor
from parameters.models import UserAgent


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

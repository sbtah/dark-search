"""
Pytest fixtures for api service.
"""
import pytest
from crawled.models.domain import Domain
from crawled.models.entity import Entity
from crawled.models.webpage import Webpage, Data


@pytest.fixture
def example_entity():
    return Entity.objects.create(name='test-entity')


@pytest.fixture
def example_domain():
    return Domain.objects.create(value='test.com')


@pytest.fixture
def example_domain_with_webpages(example_domain):
    for _ in range(5):
        Webpage.objects.create(parent_domain=example_domain, url=f'http://test.com/page-{_}')
    return example_domain


@pytest.fixture
def example_webpage(example_domain):
    return Webpage.objects.create(parent_domain=example_domain, url='http://test.com')


@pytest.fixture
def example_linked_webpage(example_webpage):
    domain: str = 'some-other-test-domain.onion'
    parent_domain: Domain = Domain.objects.create(value=domain)
    list_of_webpages: list = [
        Webpage.objects.create(url=f'htttp://{domain}/page-{_}', parent_domain=parent_domain) for _ in range(1, 11)
    ]
    for webpage in list_of_webpages:
        webpage.linking_to_webpages.add(example_webpage)
    return example_webpage


@pytest.fixture
def example_webpage_with_data(example_webpage):
    Data.objects.create(
        webpage=example_webpage,
    )
    return example_webpage


@pytest.fixture
def collection_of_domains():
    return ['domain1.onion', 'domain2.onion', 'domain3.onion', 'domain3.onion', 'domain4.onion']


@pytest.fixture
def collection_of_tags() -> list[str]:
    return ['Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5']


@pytest.fixture
def collection_of_webpages_urls():
    return [
        'http://some-page.onion/page1',
        'http://some-page-2.onion/page2',
        'http://some-page.onion/page3',
        'http://some-page.onion/page1',  # Duplicated!
        'http://some-page.onion/page-other',
        'http://other.onion/page1',
    ]

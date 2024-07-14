"""
Pytest fixtures for api service.
"""
import pytest
from crawled.models.domain import Domain
from crawled.models.entity import Entity
from crawled.models.webpage import Webpage


@pytest.fixture
def example_entity():
    return Entity.objects.create(name='test-entity')


@pytest.fixture
def example_domain():
    return Domain.objects.create(value='test.com')


@pytest.fixture
def example_linked_domain(example_domain):
    list_of_domains = [Domain.objects.create(value=f'test-{_}.onion') for _ in range(1, 11)]
    for idx, domain in enumerate(list_of_domains):
        if idx % 2 == 0:
            domain.linking_to.add(example_domain)
    return example_domain


@pytest.fixture
def collection_of_domains():
    return ['domain1.onion', 'domain2.onion', 'domain3.onion', 'domain3.onion', 'domain4.onion']


@pytest.fixture
def example_webpage(example_domain):
    return Webpage.objects.create(parent_domain=example_domain, url='http://test.com')

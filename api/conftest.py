"""
Pytest fixtures for api service.
"""
import pytest
from crawled.models import Entity, Domain, Webpage


@pytest.fixture
def example_entity():
    return Entity.objects.create(name='test-entity')

@pytest.fixture
def example_domain():
    return Domain.objects.create(value='test.com')

@pytest.fixture
def example_webpage(example_domain):
    return Webpage.objects.create(parent_domain=example_domain, url='http://test.com')

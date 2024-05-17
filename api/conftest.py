"""
Pytest fixtures for api service.
"""
import pytest
from crawled.models import Entity, Domain


@pytest.fixture
def example_entity():
    return Entity.objects.create(name='test-entity')

@pytest.fixture
def example_domain():
    return Domain.objects.create(value='test.com')

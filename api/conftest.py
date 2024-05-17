"""
Pytest fixtures for api service.
"""
import pytest
from crawled.models import Entity


@pytest.fixture
def entity():
    return Entity.objects.create(name='test-entity')
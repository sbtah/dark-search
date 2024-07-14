import pytest
from crawled.models.entity import Entity


pytestmark = pytest.mark.django_db


class TestEntityModel:
    """Test cases for the Entity object."""

    def test_create_entity(self):
        """Test creating an entity object is successful."""
        assert Entity.objects.count() == 0
        entity = Entity.objects.create(name='test-entity')
        assert Entity.objects.count() == 1
        assert isinstance(entity, Entity)

    def test_entity_str_method(self):
        """Test that Entity __str__ is generating desired output."""
        entity = Entity.objects.create(name='test-entity')
        assert str(entity) == entity.name

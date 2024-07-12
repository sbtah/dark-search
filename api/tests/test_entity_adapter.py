"""
Test cases for EntityAdapter class.
"""
import pytest
from crawled.models import Entity
from logic.adapters.entity import EntityAdapter
from unittest.mock import MagicMock


pytestmark = pytest.mark.django_db


@pytest.fixture
def adapter() -> EntityAdapter:
    adapter: EntityAdapter = EntityAdapter()
    adapter.logger = MagicMock()
    return adapter


class TestEntityAdapter:
    """Test cases for EntityAdapter functionality."""

    def test_entity_adapter_sync_get_or_create_entity_getting_successful(
        self,
        adapter,
        example_entity,
    ) -> None:
        """
        Test that sync_get_or_create_entity is successfully fetching Entity objects from db.
        """
        return_value = adapter.sync_get_or_create_entity(name='test-entity')
        assert isinstance(return_value, Entity)

    def test_entity_adapter_sync_get_or_create_entity_create_entity_with_name_only(
        self,
        adapter,
    ) -> None:
        """
        Test that sync_get_or_create_entity successfully creates new Entity object.
        """
        assert Entity.objects.count() == 0
        return_value = adapter.sync_get_or_create_entity(name='test-entity')
        assert Entity.objects.count() == 1
        assert return_value.name == 'test-entity'

    def test_entity_adapter_sync_get_or_create_entity_create_entity_with_extra_data(
        self,
        adapter,
    ) -> None:
        """
        Test that sync_get_or_create_entity is creating new Entity with all additional data.
        """
        assert Entity.objects.count() == 0
        name: str = 'test-entity'
        description: str = 'Some test Entity'
        additional_data: dict = {'btc_wallet': 'test', 'telegram': 'test2'}
        creation_data = {
            'name': name,
            'description': description,
            'additional_data': additional_data,
        }
        return_value = adapter.sync_get_or_create_entity(**creation_data)
        assert Entity.objects.count() == 1
        assert return_value.name == name
        assert return_value.description == description
        assert return_value.additional_data == additional_data


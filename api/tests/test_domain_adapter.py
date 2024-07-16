"""
Test cases for DomainAdapter class.
"""
from unittest.mock import MagicMock

import pytest
from crawled.models.domain import Domain
from logic.adapters.domain import DomainAdapter


pytestmark = pytest.mark.django_db


@pytest.fixture
def adapter() -> DomainAdapter:
    """
    Fixture returning instance of DomainAdapter.
    Logging is turned off in testing.
    """
    adapter: DomainAdapter = DomainAdapter()
    adapter.logger = MagicMock()
    adapter.tag_adapter.logger = MagicMock()
    return adapter


class TestDomainAdapter:
    """Test cases for DomainAdapter feature."""

    def test_domain_adapter_get_or_create_domain_by_value_return_existing_object(
        self,
        adapter,
        example_domain,
    ) -> None:
        """
        Test that get_or_create_domain_by_value is successfully fetching a Domain object from db.
        """
        return_value = adapter.get_or_create_domain_by_value(value='test.com')
        assert isinstance(return_value, Domain)

    def test_domain_adapter_get_or_create_domain_by_value_create_new_object(
        self,
        adapter,
    ) -> None:
        """
        Test that get_or_create_domain_by_value successfully creates a new Domain object.
        """
        assert Domain.objects.count() == 0
        return_value = adapter.get_or_create_domain_by_value(value='some-domain.onion')
        assert Domain.objects.count() == 1
        assert return_value.value == 'some-domain.onion'

    def test_domain_adapter_update_domain_is_successful(
        self,
        adapter,
        example_domain,
        example_entity,
        collection_of_tags,
    ) -> None:
        """Test that update_domain is properly updating fields on a Domain object."""
        return_value = adapter.update_domain(
            domain=example_domain,
            parent_entity=example_entity,
            favicon_base64='Test base64',
            server='test-server',
            last_crawl_date=10565,
            number_of_crawls=2,
            number_of_successful_crawls=2,
            average_crawl_time=22,
            domain_rank=1.77,
            tags=collection_of_tags,
            site_structure={'key': 'value'},
        )
        assert isinstance(return_value, Domain)
        assert return_value.parent_entity == example_entity
        assert return_value.favicon_base64 == 'Test base64'
        assert return_value.server == 'test-server'
        assert return_value.last_crawl_date == 10565
        assert return_value.number_of_crawls == 2
        assert return_value.number_of_successful_crawls == 2
        assert return_value.average_crawl_time == 22
        assert return_value.domain_rank == 1.77
        assert return_value.tags.count() == 5
        assert return_value.site_structure == {'key': 'value'}

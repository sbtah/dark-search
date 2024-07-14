import pytest
from crawled.models import Domain


pytestmark = pytest.mark.django_db


class TestDomainModel:
    """Test cases for the Domain model."""

    def test_create_domain(self) -> None:
        """Test creating Domain is successful."""
        assert Domain.objects.count() == 0
        domain = Domain.objects.create(value='test.com')
        assert Domain.objects.count() == 1
        assert isinstance(domain, Domain)

    def test_domain_save_method(self) -> None:
        """Test that Domain's save method is properly saving data only on creation."""
        domain = Domain.objects.create(value='test.com')
        current_created = domain.created
        assert current_created is not None
        domain.value = 'new-test.com'
        domain.save()
        domain.refresh_from_db()
        assert current_created == domain.created
        assert isinstance(domain.created, int)

    def test_domain_str_method(self) -> None:
        """Test that Domain's str method is generating proper output."""
        domain = Domain.objects.create(value='test.com')
        assert str(domain) == domain.value

    def test_domain_linking_to_field_and_properties(self, example_linked_domain) -> None:
        """Test linking_to field and all based properties on the Domain object."""
        assert len(example_linked_domain.linking_from) == 5
        assert example_linked_domain.num_of_linking_from_domains == 5
        assert len(example_linked_domain.linking_to.all()) == 0
        assert example_linked_domain.num_of_linking_to_domains == 0

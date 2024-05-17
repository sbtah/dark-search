import pytest
from crawled.models import Domain


pytestmark = pytest.mark.django_db


class TestDomainObject:
    """Test cases for Domain model."""

    def test_create_domain(self):
        """Test creating Domain is successful."""
        assert Domain.objects.count() == 0
        domain = Domain.objects.create(
            value='test.com',
        )
        assert Domain.objects.count() == 1

    def test_domain_save_method(self):
        """Test that Domain's save method is properly saving data only on creation"""
        assert Domain.objects.count() == 0
        domain = Domain.objects.create(
            value='test.com',
        )
        current_created = domain.created
        assert current_created is not None
        domain.value = 'new-test.com'
        domain.save()
        domain.refresh_from_db()
        assert current_created == domain.created
        assert isinstance(current_created, int)

    def test_domain_str_method(self):
        """Test that Domain's str method is generating proper output."""
        domain = Domain.objects.create(
            value='test.com',
        )
        assert str(domain) == domain.value

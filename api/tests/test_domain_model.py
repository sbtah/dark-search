"""
Test cases for the Domain model.
"""
import pytest
from crawled.models.domain import Domain


pytestmark = pytest.mark.django_db


class TestDomainModel:
    """Test cases for the Domain model."""

    def test_create_domain(self) -> None:
        """Test creating Domain is successful."""
        assert Domain.objects.count() == 0
        domain = Domain.objects.create(value='test.com')
        assert Domain.objects.count() == 1
        assert isinstance(domain, Domain)

    def test_domain_str_method(self) -> None:
        """Test that Domain's str method is generating proper output."""
        domain = Domain.objects.create(value='test.com')
        assert str(domain) == domain.value

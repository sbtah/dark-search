# """
# Test cases for Webpage object.
# """
import pytest
from crawled.models.webpage import Webpage
from django.db.utils import IntegrityError


pytestmark = pytest.mark.django_db


class TestWebpageModel:
    """Test cases for the Webpage model."""

    def test_create_webpage(self, example_domain):
        """Test creating Webpage object is successful."""
        assert Webpage.objects.count() == 0
        webpage = Webpage.objects.create(parent_domain=example_domain, url='http://test.com')
        assert Webpage.objects.count() == 1
        assert isinstance(webpage, Webpage)

    def test_webpage_str_method(self, example_domain):
        """Test that Webpage's str method is generating proper output"""
        webpage = Webpage.objects.create(parent_domain=example_domain, url='http://test.com')
        assert str(webpage) == webpage.url

    def test_webpage_is_homepage_unique_constraint(self, example_domain):
        """Test that only one Webpage can have is_homepage field set to True."""
        webpage_1 = Webpage.objects.create(parent_domain=example_domain, url='http://test.com', is_homepage=True)
        assert webpage_1.is_homepage is True
        assert Webpage.objects.count() == 1
        with pytest.raises(IntegrityError):
            Webpage.objects.create(parent_domain=example_domain, url='http://test-second.com', is_homepage=True)
            assert Webpage.objects.count() == 1

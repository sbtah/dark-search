# """
# Test cases for Webpage objects.
# """
import pytest
from crawled.models import Webpage

pytestmark = pytest.mark.django_db


class TestWebpageModel:
    """Test cases for Webpage model."""

    def test_create_webpage(self, example_domain):
        """Test creating Webpage object is successful."""
        assert Webpage.objects.count() == 0
        webpage = Webpage.objects.create(parent_domain=example_domain, url='http://test.com')
        assert Webpage.objects.count() == 1
        assert isinstance(webpage, Webpage)

    def test_webpage_save_method(self, example_domain):
        """Test that Webpage's save method is properly setting created at value only once."""
        webpage = Webpage.objects.create(parent_domain=example_domain, url='http://test.com')
        current_created = webpage.created
        assert webpage.created is not None
        webpage.url = 'http://new-test.com'
        webpage.save()
        webpage.refresh_from_db()
        assert current_created == webpage.created
        assert isinstance(webpage.created, int)

    def test_webpage_str_method(self, example_domain):
        """Test that Webpage's str method is generating proper output"""
        webpage = Webpage.objects.create(parent_domain=example_domain, url='http://test.com')
        assert str(webpage) == webpage.url

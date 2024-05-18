# """
# Test cases for tasks objects.
# """
import pytest
from tasks.models import CrawlTask

pytestmark = pytest.mark.django_db


class TestCrawlTaskModel:
    """Test cases for CrawlTask model."""

    def test_create_crawltask(self):
        """Test creating CrawlTask object is successful."""
        assert CrawlTask.objects.count() == 0
        crawl = CrawlTask.objects.create(
            domain='test.com',
        )
        assert CrawlTask.objects.count() == 1
        assert isinstance(crawl, CrawlTask)

    def test_crawltask_str_method(self):
        """Test that CrawlTask's __str__ is generating proper output."""
        crawl = CrawlTask.objects.create(
            domain='test.com',
        )
        assert str(crawl) == 'CrawlTask:test.com'

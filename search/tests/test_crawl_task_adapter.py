"""
Test cases for CrawlTask adapter.
"""
from datetime import datetime, timedelta

import pytest
from django.db.models import QuerySet
from logic.adapters.task import CrawlTaskAdapter
from logic.exceptions.adapters.task import (
    NoActiveTasksError,
    NoTaskValueProvidedError,
)
from tasks.models import CrawlTask
from unittest.mock import MagicMock


pytestmark = pytest.mark.django_db


@pytest.fixture
def example_tasks() -> None:
    """Fixture for generating 10 test CrawlTask objects."""
    date = datetime.now()
    for _ in range(11):
        days = timedelta(_)
        date_of_creation = date + days
        stamp = int(datetime.timestamp(date_of_creation))
        CrawlTask.objects.create(
            domain=f'example-{_}.onion', last_launch_date=stamp, importance=_
        )


@pytest.fixture
def example_active_task() -> CrawlTask:
    return CrawlTask.objects.create(domain='example.onion')


@pytest.fixture
def example_finished_task() -> CrawlTask:
    return CrawlTask.objects.create(domain='example.onion', status='FINISHED', current_celery_id='TEST ID')


@pytest.fixture
def example_taken_task() -> CrawlTask:
    return CrawlTask.objects.create(
        domain='example.onion',
        status='TAKEN',
        current_celery_id='TEST ID',
        average_time_to_finish=2,
        number_of_finished_launches=1,
    )


@pytest.fixture
def adapter():
    adapter = CrawlTaskAdapter()
    adapter.logger = MagicMock()
    return adapter


class TestCrawlTaskAdapter:
    """Test cases for adapter functionality for CrawlTask."""

    def test_crawl_task_adapter_get_active_task(self, adapter, example_tasks):
        """
        Test that _get_active_task method is returning properly ordered Queryset.
        Method is filtering tasks by last_launch_date ascending and by highest importance descending.
        """
        active_tasks = adapter._get_active_tasks()
        assert isinstance(active_tasks, QuerySet)
        assert active_tasks.first().importance == 0
        assert active_tasks.first().status == 'ACTIVE'

    def test_crawl_task_adapter_mark_task_active(self, adapter, example_finished_task):
        """Test that mark_task_active method is properly saving `ACTIVE` status."""
        result = adapter.mark_task_active(task=example_finished_task)
        assert result is True
        example_finished_task.refresh_from_db()
        assert example_finished_task.status == 'ACTIVE'
        assert example_finished_task.current_celery_id is None

    def test_crawl_task_adapter_mark_task_taken(self, adapter, example_active_task):
        """Test that mark_task_taken method is properly saving new status of CrawlTask."""
        result = adapter.mark_task_taken(
            task=example_active_task, celery_id='Test ID', launch_timestamp=11111111
        )
        assert result is True
        example_active_task.refresh_from_db()
        assert example_active_task.status == 'TAKEN'
        assert example_active_task.current_celery_id == 'Test ID'
        assert example_active_task.last_launch_date == 11111111

    def test_crawl_task_adapter_mark_task_taken_raises_exception(self, adapter, example_active_task):
        """Test that mark_task_taken method is raising exception when arguments are missing."""
        with pytest.raises(NoTaskValueProvidedError):
            adapter.mark_task_taken(task=example_active_task)

    def test_crawl_task_adapter_mark_task_failed(self, adapter, example_taken_task):
        """Test that mark_task_failed is setting expected status on CrawlTask object."""
        result = adapter.mark_task_failed(task=example_taken_task)
        assert result is True
        example_taken_task.refresh_from_db()
        assert example_taken_task.status == 'FAILED'

    def test_crawl_task_adapter_mark_task_finished(self, adapter, example_taken_task):
        """Test that mark_task_finished is properly saving all needed data on CrawlTask object."""
        date_timestamp: int = int(datetime.now().timestamp())
        result = adapter.mark_task_finished(
            task=example_taken_task, finished_timestamp=date_timestamp, crawl_time_seconds=2
        )
        assert result is True
        example_taken_task.refresh_from_db()
        assert example_taken_task.status == 'FINISHED'
        assert example_taken_task.number_of_finished_launches == 2
        assert example_taken_task.average_time_to_finish == 2
        assert example_taken_task.last_finished_date == date_timestamp

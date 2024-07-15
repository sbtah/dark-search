"""
Test cases for the Tag model.
"""
import pytest
from crawled.models.tag import Tag


pytestmark = pytest.mark.django_db


class TestTagModel:
    """Test cases for Tag model class."""

    def test_create_tag(self):
        """Test creating the Tag object is successful."""
        assert Tag.objects.count() == 0
        tag: Tag = Tag.objects.create(value='test')
        assert Tag.objects.count() == 1
        assert isinstance(tag, Tag)

    def test_tag_str_method(self):
        """Test that Tag's __str__ method is returning expected output."""
        tag: Tag = Tag.objects.create(value='test')
        assert str(tag) == 'test'

import pytest
from logic.adapters.url import UrlAdapter
from logic.exceptions.adapters.url import (
    WrongTypeProvidedError,
    WrongValueProvidedError,
)
from logic.parsers.objects.url import Url


class TestUrlObject:
    """Test cases for Url class and its adapter."""

    def test_create_url_object(self):
        """Test that Url object can be created."""
        url = UrlAdapter.create_url_object(value='test.com')
        assert isinstance(url, Url)
        assert url.value == 'test.com'

    def test_create_url_with_wrong_value_type_raises_exception(self):
        """Test that trying to create Url with the wrong type for `url.value` raises an Exception"""
        for t in [1 , 1,22, True, list, dict, set]:
            with pytest.raises(WrongTypeProvidedError):
                UrlAdapter.create_url_object(value=t)

    def test_create_url_with_wrong_length_for_value_raises_exception(self):
        """Test that trying to create Url with the wrong length for `url.value` raises an Exception"""
        with pytest.raises(WrongValueProvidedError):
            UrlAdapter.create_url_object(value='a.com')

    def test_create_url_with_wrong_anchor_type_raises_exception(self):
        """Test that trying to create Url with the wrong type for `url.anchor` raises an Exception"""
        for t in [1 , 1,22, True, list, dict, set]:
            with pytest.raises(WrongTypeProvidedError):
                UrlAdapter.create_url_object(value='test.com', anchor=t)

    def test_create_url_with_wrong_number_of_requests_type_raises_exception(self):
        """Test that trying to create Url with the wrong type for `url.number_of_requests` raises an Exception"""
        for t in ['1', list, dict, set]:
            with pytest.raises(WrongTypeProvidedError):
                UrlAdapter.create_url_object(value='test.com', number_of_requests=t)

    def test_url_serialize_returns_dict(self):
        """Test Url.serialize() method is returning dictionary."""
        url = UrlAdapter.create_url_object(value='test.com')
        serialized = url.serialize()
        assert isinstance(serialized, dict)
        assert serialized['value'] == 'test.com'

    def test_url_object_is_hashable(self):
        """Test that Url object is indeed hashable."""
        url = UrlAdapter.create_url_object(value='test.com')
        test_set = set()
        test_set.add(url)
        assert url in test_set
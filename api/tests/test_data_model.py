# """
# Test cases for Data object.
# """
import pytest
from crawled.models.webpage import Data


pytestmark = pytest.mark.django_db


class TestDataModel:
    """Test cases for the Data model."""

    def test_create_data(self, example_webpage):
        """Test creating the Data object is successful."""
        assert Data.objects.count() == 0
        data = Data.objects.create(webpage=example_webpage)
        assert Data.objects.count() == 1
        assert isinstance(data, Data)

    def test_data_str_method(self, example_webpage):
        """Test that Data's str is generating proper output."""
        data = Data.objects.create(webpage=example_webpage)
        assert str(data) == f'Data of: {data.webpage.url}'

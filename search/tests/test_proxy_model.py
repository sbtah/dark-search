# """
# Test cases for proxy objects.
# """
import pytest
from parameters.models import Proxy

pytestmark = pytest.mark.django_db


class TestProxyModel:
    """Test cases for Proxy model."""

    def test_create_proxy(self):
        """Test creating Proxy is successful."""
        assert Proxy.objects.count() == 0
        proxy = Proxy.objects.create(value='127.0.0.1')
        assert Proxy.objects.count() == 1
        assert isinstance(proxy, Proxy)

    def test_proxy_str_method(self):
        """Test that Proxy __str__ is generating proper output."""
        proxy = Proxy.objects.create(value='127.0.0.1')
        assert str(proxy) == f'{proxy.type}:{proxy.value}:{proxy.status}'

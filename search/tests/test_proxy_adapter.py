"""
Test cases for ProxyAdapter.
"""
import pytest
from logic.adapters.proxy import ProxyAdapter
from logic.exceptions.adapters.proxies import NoProxiesError
from parameters.models import Proxy


pytestmark = pytest.mark.django_db


class TestProxyAdapter:
    """Test cases for ProxyAdapter."""

    def test_get_proxy(self, many_proxies):
        """Test that get_proxy method is retrieving the least used Proxy."""
        proxies = Proxy.objects.all()
        assert len(proxies) > 1
        proxy = ProxyAdapter().get_proxy()
        assert isinstance(proxy, Proxy)
        assert proxy.current_spiders == 1

    def test_get_proxy_raises_exception(self):
        """Test that get_proxy is raising NoProxiesError if no proxies were found in database."""
        with pytest.raises(NoProxiesError):
            ProxyAdapter().get_proxy()

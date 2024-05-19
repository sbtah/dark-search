from logic.adapters.base import BaseAdapter
from logic.exceptions.adapters.proxies import NoProxiesError
from parameters.models import Proxy


class ProxyAdapter(BaseAdapter):
    """Adapter for managing Proxy objects."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy = Proxy

    def get_proxy(self) -> Proxy:
        """Retrieve the least used Proxy from database."""
        proxies = self.proxy.objects.all().order_by('current_spiders')
        if not proxies:
            raise NoProxiesError()
        return proxies.first()

from logic.adapters.base import BaseAdapter
from logic.exceptions.adapters.proxy import NoProxiesError
from parameters.models import Proxy


class ProxyAdapter(BaseAdapter):
    """Adapter for managing Proxy objects."""

    def __init__(self, *args, **kwargs):
        self.proxy = Proxy
        super().__init__(*args, **kwargs)

    def get_proxy(self) -> Proxy:
        """Retrieve the least used Proxy from the database."""
        proxies = self.proxy.objects.all().order_by('current_spiders')
        if not proxies:
            raise NoProxiesError()
        return proxies.first()

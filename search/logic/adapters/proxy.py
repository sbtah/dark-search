from logic.adapter.base import BaseAdapter
from parameters.models import Proxy


class ProxyAdapter(BaseAdapter):
    """Adapter for managing Proxy objects."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy = Proxy

    def get_proxy(self) -> Proxy:
        """Retrieve least used Proxy from database."""
        proxies = self.proxy.objects.all().orderby('current_spiders')
        return proxies.first()
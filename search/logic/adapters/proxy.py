from typing import Any

from django.db.models import QuerySet
from logic.adapters.base import BaseAdapter
from logic.exceptions.adapters.proxy import NoProxiesError
from parameters.models import Proxy


class ProxyAdapter(BaseAdapter):
    """Adapter for managing Proxy objects."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.proxy: Proxy = Proxy
        super().__init__(*args, **kwargs)

    def sync_get_or_create_proxy(self, proxy: str) -> Proxy:
        """
        Create a new Proxy object or return existing one.
        - :arg proxy: String representing Proxy value.
        """
        try:
            existing_proxy: Proxy = self.proxy.objects.get(value=proxy)
            self.logger.debug(f'Proxy Adapter, found existing Proxy: proxy_id="{existing_proxy.id}", value="{proxy}"')
            return existing_proxy
        except Proxy.DoesNotExist:
            new_proxy: Proxy = self.proxy.objects.create(value=proxy)
            self.logger.debug(f'Proxy Adapter, created new Proxy: proxy_id="{new_proxy.id}", value="{proxy}"')
            return new_proxy

    def get_proxy(self) -> Proxy:
        """Retrieve the least used Proxy from the database."""
        proxies: QuerySet[Proxy] = self.proxy.objects.all().order_by('current_spiders')
        if not proxies:
            raise NoProxiesError()
        return proxies.first()

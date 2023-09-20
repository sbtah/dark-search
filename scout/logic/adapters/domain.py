from logic.adapters.base import BaseAdapter
from domains.models import Domain


class DomainAdapter(BaseAdapter):
    """
    Simple adapter to help fetching and interacting with Domain objects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = Domain

    async def get_or_create_domain(self, domain: str) -> Domain:
        """
        Finds or creates a Domain object with provided domain address.
        - :arg domain: Domain address.
        """
        try:
            existing_domain = await self.domain.objects.aget(value=domain)
            return existing_domain
        except Domain.DoesNotExist:
            new_domain = await self.domain.objects.acreate(value=domain)
            return new_domain

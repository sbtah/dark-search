from logic.adapters.base import BaseAdapter
from crawled.models import Domain, Entity


class DomainAdapter(BaseAdapter):
    """
    Adapter class for managing Domain objects.
    """

    def __init__(self) -> None:
        self.domain: Domain = Domain
        super().__init__()

    def get_or_create_domain(
        self,
        value: str,
        favicon_base64: str | None = None,
        server: str | None = None,

    ) -> Domain:
        """"""
        ...

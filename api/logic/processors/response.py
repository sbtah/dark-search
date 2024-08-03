from logic.processors.base import BaseProcessor
from logic.adapters.entity import EntityAdaper
from logic.adapters.domain import DomainEntity
from logic.adapers.tag import TagAdapter
from logic.adapters.webpage import WebpageAdapter
from crawled.models.domain import Domain
from crawled.models.webpage import Webpage


class ResponseProcessor(BaseProcessor):
    """
    Crawler's response processor.
    Here data received from crawler is parsed
    and new objects are created or updated.
    """
    def __init__(self) -> None:
        self.entity_adapter: EntityAdaper = EntityAdaper()
        self.domain_adapter: DomainEntity = DomainEntity()
        self.webpage_adapter: WebpageAdapter = WebpageAdapter()
        self.tag_adapter: TagAdapter = TagAdapter()


    def parse(self):
        ...

    def process_response(self, response: dict):
        """"""
        href: str = response['requested_url']['value']
        anchor: str = response['requested_url']['anchor']
        number_of_requests: int = response['requested_url']['number_of_requests']

        status: str | None = response['status']
        responded_url: str | None = response['responded_url']
        server: str | None = response['server']
        elapsed: int | None = response['elapsed']
        visited: int | None = response['visited']
        text: str | None = response['text']
        page_title: str | None = response['page_title']
        meta_title: str | None = response['meta_title']
        meta_description: str | None = response['meta_description']
        on_page_urls: list[dict] | None = response['on_page_urls']
        processed_urls: dict | None = response['processed_urls']

        # Extract value of domain from requested url.
        domain_value: str = self.domain_adapter.extract_domain(url=href)

        # Create Domain object for further processing.
        current_domain: Domain = self.domain_adapter.get_or_create_domain_by_value(
            value=domain_value,
        )

        # Create Webpage object.
        current_webpage: Webpage = self.webpage_adapter.get_or_create_webpage_by_url(
            url=href, domain=current_domain
        )

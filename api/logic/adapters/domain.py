from datetime import date
from typing import Collection

from crawled.models.domain import Domain
from crawled.models.entity import Entity
from logic.adapters.base import BaseAdapter
from logic.adapters.tag import Tag, TagAdapter
from urllib.parse import urlsplit


class DomainAdapter(BaseAdapter):
    """
    Adapter class for managing Domain objects.
    """

    def __init__(self) -> None:
        self.domain: Domain = Domain
        self.tag_adapter: TagAdapter = TagAdapter()
        super().__init__()

    @staticmethod
    def extract_domain(*, url: str) -> str:
        """
        Extract domain value from url.
        - :arg url: String representing provided url.
        """
        domain: str = urlsplit(url).netloc
        return domain

    def get_number_of_known_domains(self) -> int:
        """
        Return number of all existing Domain objects in database.
        """
        number_of_known_domains: int = self.domain.objects.count()
        return number_of_known_domains

    def get_number_of_crawled_domains(self) -> int:
        """
        Return number of all already crawled Domains.
        """
        number_of_crawled_domains: int = self.domain.objects.filter(last_crawl_date__isnull=False).count()
        return number_of_crawled_domains

    def get_or_create_domain_by_value(self, *, value: str) -> Domain:
        """
        Create a new Domain object or return existing one.
        - :arg value: String representing a Domain value.
        """
        try:
            existing_domain: Domain = self.domain.objects.get(value=value)
            self.logger.debug(f'DomainAdapter, found existing Domain: domain_id="{existing_domain.id}, value="{value}"')
            return existing_domain
        except Domain.DoesNotExist:
            new_domain: Domain = self.domain.objects.create(value=value)
            self.logger.debug(f'DomainAdapter, created new Domain: domain_id="{new_domain.id}, value="{value}"')
            return new_domain

    def update_domain(
        self,
        *,
        domain: Domain,
        parent_entity: Entity | None = None,
        favicon_base64: str | None = None,
        server: str | None = None,
        last_crawl_date: date | None = None,
        number_of_crawls: int | None = None,
        number_of_successful_crawls: int | None = None,
        average_crawl_time: int | None = None,
        domain_rank: float | None = None,
        tags: Collection[str] | None = None,
        site_structure: dict | None = None,
    ) -> Domain:
        """
        Update a Domain object.
        Updates on M2M fields are clearing fields first.
        - :arg domain: Domain objects to be updated.
        - :arg parent_entity: Entity object parent that we want to change or add.
        - :arg favicon_base_64: String representing favicon image in base64 format.
        - :arg server: String representing server technology used for hosting domain.
        - :arg last_crawl_date: Date object representing date of last crawl.
        - :arg number_of_crawls: Integer representing number of launched crawls for Domain.
        - :arg number_of_successful_crawls: Integer representing number of successful crawls for Domain.
        - :arg average_crawl_time: Integer representing time in seconds needed for crawling entire Domain.
        - :arg domain_rank: Float representing rank of Domain,
        - :arg site_structure: Dictionary/Json representing a mapping of Domain's structure.
        """
        if parent_entity is not None:
            domain.parent_entity = parent_entity

        if favicon_base64 is not None:
            domain.favicon_base64 = favicon_base64

        if server is not None:
            domain.server = server

        if last_crawl_date is not None:
            domain.last_crawl_date = last_crawl_date

        if number_of_crawls is not None:
            domain.number_of_crawls = number_of_crawls

        if number_of_successful_crawls is not None:
            domain.number_of_successful_crawls = number_of_successful_crawls

        if average_crawl_time is not None:
            domain.average_crawl_time = average_crawl_time

        if domain_rank is not None:
            domain.domain_rank = domain_rank

        if tags is not None:
            domain.tags.clear()
            collection_of_tags: list[Tag] = [
                self.tag_adapter.get_or_create_tag(value=tag_value) for tag_value in tags
            ]
            for found_tag in collection_of_tags:
                domain.tags.add(found_tag)

        if site_structure is not None:
            domain.site_structure = site_structure

        domain.save()
        self.logger.debug(f'DomainAdapter, updated Domain: domain_id="{domain.id}"')
        return domain

from crawled.models import Domain
from libraries.adapters.base import BaseAdapter


class DomainAdapter(BaseAdapter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = Domain

    @staticmethod
    def calculate_average_crawl_time(domain: Domain, last_crawl_time: int):
        """"""
        if domain.average_crawl_time is not None:
            domain.average_crawl_time = (domain.average_crawl_time + last_crawl_time) / domain.number_of_crawls_finished
        else:
            domain.average_crawl_time = last_crawl_time
        return domain

    def update_or_create_domain(
        self,
        value: str = None,
        last_crawl_date: int = None,
        # For calculating average crawl time.
        last_crawl_time: int = None,
        server: str = None,
        description: str = None,
        number_of_crawls_finished: int = None,
        number_of_pages_found: int = None
    ):
        """
        Create or update existing Domain object.
        """
        try:
            existing_domain = self.domain.objects.get(
                value=value,
            )
            if last_crawl_date is not None:
                existing_domain.last_crawl_date = last_crawl_date
            if server is not None:
                existing_domain.server = server
            if description is not None:
                existing_domain.description = description
            if number_of_crawls_finished is not None:
                existing_domain.number_of_crawls_finished += number_of_crawls_finished
            if number_of_pages_found is not None:
                existing_domain.number_of_pages_found = number_of_pages_found
            # TODO:
            if last_crawl_time is not None:
                existing_domain = self.calculate_average_crawl_time(
                    domain=existing_domain,
                    last_crawl_time=last_crawl_time,
                )

            existing_domain.save()
            self.logger.debug(f'API: Updated Domain: {existing_domain}')
            return existing_domain
        except self.domain.DoesNotExist:
            creation_data = {
                'value': value,
            }
            if last_crawl_date is not None:
                creation_data['last_crawl_date'] = last_crawl_date
            if last_crawl_time is not None:
                creation_data['average_crawl_time'] = last_crawl_time
            if server is not None:
                creation_data['server'] = server
            if description is not None:
                creation_data['description'] = description

            new_domain = self.domain.objects.create(**creation_data)
            self.logger.debug(f'API: Created new Domain: {new_domain}')
            return new_domain

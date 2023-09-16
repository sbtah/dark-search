from crawled.models import Domain
from libraries.adapters.base import BaseAdapter


class DomainAdapter(BaseAdapter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = Domain

    def update_or_create_domain(
        self,
        domain: str,
        title: str = None,
        description: str = None,
        server: str = None,
    ):
        """
        Create or update existing Domain object.
        """
        try:
            existing_domain = self.domain.objects.get(
                value=domain,
            )
            if title is not None and not existing_domain.title:
                existing_domain.title = title
            if description is not None and not existing_domain.description:
                existing_domain.description = description
            if server is not None:
                existing_domain.server = server

            existing_domain.save()
            self.logger.info(f'API: Updated Domain: {existing_domain}')
            return existing_domain
        except Domain.DoesNotExist:
            creation_data = {
                'value': domain,
            }
            if title is not None:
                creation_data['title'] = title
            if description is not None:
                creation_data['description'] = description
            if server is not None:
                creation_data['server'] = server

            new_domain = self.domain.objects.create(**creation_data)
            self.logger.info(f'API: Created new Domain: {new_domain}')
            return new_domain

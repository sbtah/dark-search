from libraries.adapters.base import BaseAdapter
from tasks.models import Task
from domains.models import Domain


class DomainAdapter(BaseAdapter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = Domain
        self.task = Task

    async def get_or_create_domain(self, domain: str):
        """"""
        try:
            existing_domain = await self.domain.objects.aget(value=domain)
            return existing_domain
        except Domain.DoesNotExist:
            new_domain = await self.domain.objects.acreate(value=domain)
            related_task = await self.task.objects.acreate(owner=new_domain)
            self.logger.info(f'Created new Domain: {new_domain}')
            return new_domain

    async def create_domain(self, domain):
        """"""
        try:
            new_domain = await self.domain.objects.acreate(value=domain)
            related_task = await self.task.objects.acreate(owner=new_domain)
            self.logger.info(f'Created new Domain: {new_domain} and related Task: {related_task}')
            return new_domain
        except Exception as e:
            self.logger.error(f'(update_or_create_domain) Some other exception: {e}')
            raise

    async def get_domain(self, domain: str):
        """"""
        try:
            domain_object = self.domain.objects.aget(value=domain)
            return domain_object
        except Domain.DoesNotExist:
            return None

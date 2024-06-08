from logic.adapters.base import BaseAdapter
from tasks.models import CrawlTask


class CrawlTaskAdapter(BaseAdapter):
    """Adapter for interacting with CrawlTasks objects."""
    
    def __init__(self, *args, **kwargs):
        self.task = CrawlTask
        super().__init__(*args, **kwargs)


    def get_active_task(self):
        """Get first ACTIVE Task object for crawling."""
        # TODO:
        task = self.task.objects.filter(status=CrawlTask.status.active).order_by('last_launch_day')
        ...

    async def async_get_or_create_task(self, domain: str) -> int:
        """
        Try to create a new Task object or return existing one.
        Return Task id.
        - :arg domain: String with domain value.
        """
        try:
            existing_task = await self.task.objects.aget(domain=domain)
            return existing_task.id
        except CrawlTask.DoesNotExist:
            new_task = await self.task.objects.acreate(domain=domain)
            return new_task.id

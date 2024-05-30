from logic.adapters.base import BaseAdapter
# from logic.exceptions.adapters.proxies import NoProxiesError
from tasks.models import CrawlTask


class CrawlTaskAdapter(BaseAdapter):
    """Adapter for interacting with CrawlTasks objects."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = CrawlTask

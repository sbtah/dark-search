from logic.adapters.base import BaseAdapter
from crawled.models.webpage import Data, Webpage


class DataAdapter(BaseAdapter):
    """
    Adapter class for managing Data objects.
    """

    def __init__(self) -> None:
        self.data: Data = Data
        super().__init__()

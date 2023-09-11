from utilities.logging import logger
from urllib.parse import urlsplit


class BaseAdapter:

    def __init__(self):
        self.logger = logger

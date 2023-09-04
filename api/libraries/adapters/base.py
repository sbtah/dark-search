from utilities.logging import logger
from urllib.parse import urlsplit


class BaseAdapter:

    def __init__(self):
        self.logger = logger

    @staticmethod
    def get_domain(url):
        domain = urlsplit(url).netloc
        if domain:
            return domain

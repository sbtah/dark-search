import os
import time
import httpx
from dotenv import load_dotenv


load_dotenv()


class TorScoutApiClient:

    def __init__(self, key=os.environ.get('API_KEY'), url=os.environ.get('API_URL')):
        self.key = key
        self.url = url


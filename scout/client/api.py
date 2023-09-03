import os
import time
import httpx
from dotenv import load_dotenv
import json

load_dotenv()


class TorScoutApiClient:

    def __init__(self, key=os.environ.get('API_KEY'), url=os.environ.get('API_URL'), client=httpx.Client()):
        self.key = key
        self.url = url
        self.client = client
        self.URLS_ENDPOINT = f'{self.url}/api/process/'

    def get(self, url):
        response = self.client.get(url, follow_redirects=True)
        return  response

    def post(self, url, data):
        response = self.client.post(url, json=json.dumps(data))
        return response

    def get_home(self):

        url = f'{self.url}/api'

        response = self.get(url)

        return response.json()

    def post_urls(self, data):

        response = self.post(self.URLS_ENDPOINT, data)

        return response.json()

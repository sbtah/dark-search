import asyncio
import os
import time
import httpx
from dotenv import load_dotenv
import json
from utilities.logging import logger


load_dotenv()


class TorScoutApiClient:

    def __init__(self, key=os.environ.get('API_KEY'), url=os.environ.get('API_URL')):
        self.key = key
        self.url = url
        self.logger = logger
        self.RESPONSE_ENDPOINT = f'{self.url}/api/process-response/'
        self.HOME_ENDPOINT = f'{self.url}/api/'
        self.UNCRAWLED_ENDPOINT = f'{self.url}/api/get-not-crawled/'

    async def get(self, url: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()
        except Exception as e:
            self.logger.error(f'(get) Some other exception: {e}')
            raise

    async def post(self, url, data):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=json.dumps(data))
                return response.json()
        except Exception as e:
            self.logger.error(f'(post) Some other exception: {e}')
            raise

    async def get_home(self):
        try:
            tasks = [asyncio.create_task(
                self.get(self.HOME_ENDPOINT)
            )]
            responses = await asyncio.gather(*tasks)
            return responses[0]
        except Exception as e:
            self.logger.error(f'(get_home) Some other exception: {e}')
            raise

    async def post_response_data(self, data):
        try:
            tasks = [asyncio.create_task(
                self.post(self.RESPONSE_ENDPOINT, data=data)
            )]
            responses = await asyncio.gather(*tasks)
            return responses[0]
        except Exception as e:
            self.logger.error(f'(post_response_data) Some other exception: {e}')
            raise

    async def get_not_crawled_website(self):
        try:
            tasks = [asyncio.create_task(
                self.get(self.UNCRAWLED_ENDPOINT)
            )]
            responses = await asyncio.gather(*tasks)
            if responses:
                return responses[0]
            return None
        except Exception as e:
            self.logger.error(f'(get_not_crawled_website) Some other exception: {e}')
            return None

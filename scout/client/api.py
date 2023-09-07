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
        self.RESPONSE_ENDPOINT = f'{self.url}/api/process/'

    async def get(self, url: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response
        except Exception as e:
            self.logger.error(f'(get) Some other exception: {e}')
            raise

    async def post(self, url, data):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=json.dumps(data))
                return response
        except Exception as e:
            self.logger.error(f'(post) Some other exception: {e}')
            raise

    async def post_response_data(self, data):
        try:
            tasks = [asyncio.create_task(
                self.post(self.RESPONSE_ENDPOINT, data=data)
            )]
            responses = await asyncio.gather(*tasks)
            return responses
        except Exception as e:
            self.logger.error(f'(post_response_data) Some other exception: {e}')
            raise

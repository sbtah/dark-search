import asyncio
import json
import os

import httpx
from dotenv import load_dotenv
from utilities.logging import logger


load_dotenv()


class TorScoutApiClient:

    def __init__(
            self,
            key=os.environ.get('API_KEY'),
            url=os.environ.get('API_URL'),
    ):
        self.key = key
        self.url = url
        self.logger = logger
        self.RESPONSE_ENDPOINT = f'{self.url}/api/process-response/'
        self.HOME_ENDPOINT = f'{self.url}/api/'

    async def get(self, url: str):
        """
        Sends get request to specified URL.
        - :arg url: Requested URL.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()
        except Exception as e:
            self.logger.error(f'(API CLient Get) Some other exception: {e}')
            raise

    async def post(self, url: str, data: dict):
        """
        Sends post request to specified URL.
        - :arg url: Requested URL.
        - :arg data: Dictionary with prepared data.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=json.dumps(data))
                return response.json()
        except Exception as e:
            self.logger.error(f'(API CLient Post) Some other exception: {e}')
            raise

    async def get_home(self):
        """
        Requests endpoint: api/.
        """
        try:
            tasks = [asyncio.create_task(
                self.get(self.HOME_ENDPOINT)
            )]
            responses = await asyncio.gather(*tasks)
            return responses[0]
        except Exception as e:
            self.logger.error(f'(API CLient get_home) Some other exception: {e}')
            raise

    async def post_response_data(self, data: dict):
        """
        Sends response data to: api/process-response/
        """
        try:
            tasks = [asyncio.create_task(
                self.post(self.RESPONSE_ENDPOINT, data=data)
            )]
            responses = await asyncio.gather(*tasks)
            return responses[0]
        except Exception as e:
            self.logger.error(f'(API CLient post_response_data) Some other exception: {e}')
            raise

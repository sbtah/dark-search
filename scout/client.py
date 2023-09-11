import httpx
from client.api import TorScoutApiClient
import asyncio

# def get_home_response():

#     # http://comp-api:8000/api/users/token/
#     response = httpx.get('http://tor-scout-api:8000')

#     return response.json()

urls = {
    'urls': [],
}

# res = get_home_response()
data = {
    'requested_url': 'http://wclekwrf2aclunlmuikf2bopusjfv66jlhwtgbiycy5nw524r6ngioid.onion/#upvote-aDh5ekZjaG9vRjBxVzUwNWJxWE5DZz09OjqJY1W8Y9dop30uTEEPWx3m',
    'status': None,
}
# print(res)

client = TorScoutApiClient()
# print(asyncio.run(client.get_home()))
print(asyncio.run(client.get_website_to_crawl()))

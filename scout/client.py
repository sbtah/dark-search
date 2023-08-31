import httpx
from client.api import TorScoutApiClient

# def get_home_response():

#     # http://comp-api:8000/api/users/token/
#     response = httpx.get('http://tor-scout-api:8000')

#     return response.json()



# res = get_home_response()


# print(res)

client = TorScoutApiClient()
print(client.key)
print(client.url)
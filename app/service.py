import asyncio

import aiohttp



async def get_api_chukc():
    url = "https://api.chucknorris.io/jokes/random"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def get_api_country(country: str):
    url = f"https://restcountries.com/v3.1/name/{country}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return data






# print(asyncio.run(post_api("https://httpbin.org/post", )))
# print(asyncio.run(get_api("https://randomuser.me/api/")))
# print(asyncio.run(get_api(")))
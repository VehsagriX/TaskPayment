import asyncio

import aiohttp


async def get_api_chukc() -> None:
    url = "https://api.chucknorris.io/jokes/random"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return


async def get_api_country(country: str) -> None:
    url = f"https://restcountries.com/v3.1/name/{country}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            # data = await response.json()
            # return data
            return None

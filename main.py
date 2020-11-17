import asyncio

import aiohttp as aiohttp
from fastapi import FastAPI

app = FastAPI()

NUM_CONCURRENT = 18


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


@app.get("/", tags=["pajacyk"])
async def read_root():
    urls = [
        'https://www.pajacyk.pl/wp-ajax.php?kliki=1'
        for _ in range(0, NUM_CONCURRENT)
    ]
    res = []
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        for html in htmls:
            res.append(html[:100])
    return res

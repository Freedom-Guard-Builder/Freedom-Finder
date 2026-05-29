import asyncio
import aiohttp

async def test_url(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            return {
                "url": url,
                "status": response.status
            }

    except:
        return {
            "url": url,
            "status": 0
        }

async def bulk_test(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [
            test_url(session, url)
            for url in urls
        ]

        return await asyncio.gather(*tasks)

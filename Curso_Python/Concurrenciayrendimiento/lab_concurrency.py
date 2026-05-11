import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

import httpx


def fetch_sync():
    urls = ["https://httpbin.org/delay/1"] * 5
    start = time.time()

    for url in urls:
        httpx.get(url)

    print("Sync time:", round(time.time() - start, 2))


async def fetch_async():
    urls = ["https://httpbin.org/delay/1"] * 5
    start = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        await asyncio.gather(*tasks)

    print("Async time:", round(time.time() - start, 2))


async def fetch_with_limit():
    urls = ["https://httpbin.org/delay/1"] * 10
    semaphore = asyncio.Semaphore(3)

    async def fetch(url, client):
        async with semaphore:
            return await client.get(url)

    start = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [fetch(url, client) for url in urls]
        await asyncio.gather(*tasks)

    print("Limited async time:", round(time.time() - start, 2))


def heavy_task(n):
    total = 0
    for i in range(10_000_000):
        total += i
    return total


def run_cpu_test():
    start = time.time()

    with ProcessPoolExecutor() as executor:
        list(executor.map(heavy_task, [1, 2, 3, 4]))

    print("CPU time:", round(time.time() - start, 2))


if __name__ == "__main__":
    fetch_sync()
    asyncio.run(fetch_async())
    asyncio.run(fetch_with_limit())
    run_cpu_test()

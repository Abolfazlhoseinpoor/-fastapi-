import asyncio
import time
import httpx

urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]
async def run(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url , timeout= 10 )
        return response.status_code

async def main():
    start = time.time()
    task = []
    for url in urls:
        task.append(run(url))
    print(task)
    result = await asyncio.gather(*task)
    end = time.time()
    print(f"zaman {start - end:2f} ")
    print(f"result : {result}")

asyncio.run(main())

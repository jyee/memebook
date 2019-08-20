import os
import random
import time
import asyncio
from aiohttp import ClientSession

# Rate is the max possible sleep between request bursts (lower is faster).
# Concurrency is the number of requests per burst.
traffic_rate = os.environ.get("TRAFFIC_RATE") or 1
traffic_concurrency = os.environ.get("TRAFFIC_CONCURRENCY") or 5
max_req_sleep = traffic_rate / traffic_concurrency

# The url to hit
target_url = os.environ.get("TARGET_URL") or "http://localhost:5000"


async def get_url(url):
    async with ClientSession() as session:
        async with session.get(url) as resp:
            await resp.text()
            print("Get {} - status {}".format(url, resp.status))
            time.sleep(random.random() * max_req_sleep)


loop = asyncio.get_event_loop()

while True:
    tasks = []
    for i in range(traffic_concurrency):
        task = asyncio.ensure_future(get_url(target_url))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))


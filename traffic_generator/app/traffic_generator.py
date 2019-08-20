import os
import random
import string
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
target_url_params = os.environ.get("TARGET_URL_PARAMS") or "shadow=shadow"


# Async function to get a url
async def get_url(url):
    async with ClientSession() as session:
        async with session.get(url) as resp:
            await resp.text()
            print("Get {} - status {}".format(url, resp.status))
            time.sleep(random.random() * max_req_sleep)

# Async function to post to a url
async def post_url(url, data):
    async with ClientSession() as session:
        async with session.post(url, data=data) as resp:
            await resp.text()
            print("Post {} - status {}".format(url, resp.status))
            time.sleep(random.random() * max_req_sleep)

# Helper function to generate random "phrases"
def generate_message(length=30):
    letters = string.ascii_lowercase
    spaces = random.choices(range(length), k=5)
    phrase = ""
    for i in range(length):
        if i in spaces:
            phrase = phrase + " "
        else:
            phrase = phrase + random.choice(letters)
    return phrase


# Main application
loop = asyncio.get_event_loop()

while True:
    tasks = []
    for i in range(traffic_concurrency):
        if random.random() > .33:
            t = get_url(target_url + "?" + target_url_params)
        else:
            data = {'entry': generate_message()}
            t = post_url(target_url + "?" + target_url_params, data)
        task = asyncio.ensure_future(t)
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))


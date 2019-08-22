import os
import redis
import asyncio
from aiohttp import web, ClientSession
import aiohttp_jinja2
import jinja2

from datadog import statsd
from ddtrace import tracer, patch
from ddtrace.contrib.aiohttp import trace_app


redishost = os.environ.get("REDIS_HOST") or "redis-master"
redisport = os.environ.get("REDIS_PORT") or 6379


# Async function to lolcat the text
async def makelolz(text):
    async with ClientSession() as session:
        async with session.post("http://lolcat/makelolz", data={"text": text}) as resp:
            return await resp.text()

# Async function to get a doggo
async def getdoggo():
    async with ClientSession() as session:
        async with session.get("http://ip.jsontest.com") as resp:
            return await resp.text()

def get_list(request):
    if "shadow" in request.rel_url.query:
        return request.rel_url.query["shadow"]
    else:
        return "entries"

@aiohttp_jinja2.template('main.html')
async def main_page(request):
    redis_list = get_list(request)
    if request.method == "POST":
        statsd.increment("guestbook.post")
        form = await request.post()

        #responses = await asyncio.gather(
        #    makelolz(form["entry"]),
        #    #getdoggo(session)
        #)
        #print(responses)

        app.redis.lpush(redis_list, form["entry"])
        raise web.HTTPFound("/")
    else:
        statsd.increment("guestbook.view")
        entries = app.redis.lrange(redis_list, 0, -1)
        return {"entries": entries}

async def clear_entries(request):
    redis_list = get_list(request)
    statsd.increment("guestbook.clear")
    app.redis.ltrim(redis_list, 1, 0)
    raise web.HTTPFound("/")


patch(aiohttp=True)
app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('templates'))

app.redis = redis.StrictRedis(
    host=redishost,
    port=redisport,
    db=0,
    charset="utf-8",
    decode_responses=True)
app.redis.config_set("save", "1 1")

app.add_routes([
    web.route("*", "/", main_page),
    web.post("/clear", clear_entries)
])
trace_app(app, tracer, service="memebook")
web.run_app(app)

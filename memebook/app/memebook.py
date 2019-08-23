from datadog import statsd
from ddtrace import tracer, patch
patch(aiohttp=True)
patch(asyncio=True)
patch(redis=True)

from ddtrace.contrib.asyncio import context_provider
from ddtrace.contrib.aiohttp import trace_app
tracer.configure(context_provider=context_provider)

import os
import redis
import asyncio
from aiohttp import web, ClientSession
import aiohttp_jinja2
import jinja2

service_name = os.environ.get("DATADOG_SERVICE_NAME") or "memebook"
analytics = os.environ.get("DD_ANALYTICS_ENABLED") or True
redishost = os.environ.get("REDIS_HOST") or "redis-master"
redisport = os.environ.get("REDIS_PORT") or 6379


# Async function to lolcat the text
async def makelolz(text):
    with tracer.trace('asyncio.makelolz'):
        async with ClientSession() as session:
            data = {"text": text}
            headers = {
                'x-datadog-trace-id': str(tracer.current_span().trace_id),
                'x-datadog-parent-id': str(tracer.current_span().span_id),
            }
            async with session.post("http://lolcat/makelolz", data=data, headers=headers) as resp:
                return "text", await resp.text()

# Async function to get a doggo
async def getdoggo():
    async with ClientSession() as session:
        async with session.get("http://doggo/getdoggo") as resp:
            return "image", await resp.text()

def get_list(request):
    if "shadow" in request.rel_url.query:
        return request.rel_url.query["shadow"]
    else:
        return "entries"

@aiohttp_jinja2.template("main.html")
async def main_page(request):
    redis_list = get_list(request)
    if request.method == "POST":
        statsd.increment("guestbook.post")
        form = await request.post()

        tasks = [
            makelolz(form["entry"])
            getdoggo()
        ]
        responses = await asyncio.gather(*tasks)
        resp = dict(responses)
        entry = "<div class=\"entry\"><img src=\"{}\" /><span>{}</span></div>".format(resp["image"], resp["text"])

        app.redis.lpush(redis_list, entry)
        return web.HTTPFound("/")
    else:
        statsd.increment("guestbook.view")
        entries = app.redis.lrange(redis_list, 0, -1)
        return {"entries": entries}

async def clear_entries(request):
    redis_list = get_list(request)
    statsd.increment("guestbook.clear")
    app.redis.ltrim(redis_list, 1, 0)
    return web.HTTPFound("/")


app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader("templates"))

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

trace_app(app, tracer, service=service_name)
app['datadog_trace']['analytics_enabled'] = analytics
web.run_app(app)

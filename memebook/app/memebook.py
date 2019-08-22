import os
import redis

from datadog import statsd

from flask import Flask
from flask import request, redirect, render_template, url_for

import asyncio
from aiohttp import ClientSession

redishost = os.environ.get("REDIS_HOST") or "redis-master"
redisport = os.environ.get("REDIS_PORT") or 6379

app = Flask(__name__)
app.redis = redis.StrictRedis(
    host=redishost,
    port=redisport,
    db=0,
    charset="utf-8",
    decode_responses=True)
app.redis.config_set("save", "1 1")


# Async function to lolcat the text
async def makelolz(session, text):
    async with session.post("http://lolcat/makelolz", data={"text": text}) as resp:
        return await resp.text()

# Async function to get a doggo
async def getdoggo(session):
    async with session.get("http://google.com") as resp:
        return await resp.text()

# Async function to memify the post
async def memeify(text):
    with aiohttp.ClientSession() as session:
        tasks = [
            makelolz(session, text),
            getdoggo(session)
        ]
        responses = await asyncio.gather(*tasks)
    print(responses)


@app.route("/", methods=["GET", "POST"])
def main_page():
    redis_list = request.args.get("shadow") or "entries"
    if request.method == "POST":
        statsd.increment("guestbook.post")
        text = request.form["entry"]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(memeify(text))

        app.redis.lpush(redis_list, request.form["entry"])
        return redirect(url_for("main_page"))
    else:
        statsd.increment("guestbook.view")
        entries = app.redis.lrange(redis_list, 0, -1)
        return render_template("main.html", entries=entries)


@app.route("/clear", methods=["POST"])
def clear_entries():
    redis_list = request.args.get("shadow") or "entries"
    statsd.increment("guestbook.clear")
    app.redis.ltrim(redis_list, 1, 0)
    return redirect(url_for("main_page"))


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

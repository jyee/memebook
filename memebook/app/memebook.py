import os
import redis

from flask import Flask
from flask import request, redirect, render_template, url_for

# Datadog tracing and metrics
from datadog import statsd


redishost = os.environ.get("REDIS_HOST") or "redis-master"
redisport = os.environ.get("REDIS_PORT") or 6379

app = Flask(__name__)
app.redis = redis.StrictRedis(host=redishost, port=redisport, db=0, charset="utf-8", decode_responses=True)
app.redis.config_set("save", "1 1")

@app.route("/", methods=["GET", "POST"])
def main_page():
    redis_list = request.args.get("shadow") or "entries"
    if request.method == "POST":
        statsd.increment("guestbook.post")
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

# Flask
from datadog import statsd
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/getdoggo', methods = ['GET'])
def doggo():
    statsd.increment("doggo.fetch")
    r = requests.get("https://dog.ceo/api/breeds/image/random")
    data = r.json()
    return data["message"]

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)

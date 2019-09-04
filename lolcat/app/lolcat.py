import os
from datadog import initialize, statsd
from flask import Flask, request
import random

if "DD_SOCKET_PATH" in os.environ:
    initialize(socket_path = os.environ.get("DD_SOCKET_PATH"))

app = Flask(__name__)

@app.route("/makelolz", methods = ["POST"])
def lolcat():
    statsd.increment("lolcat.converted")
    return translate(request.form["text"].lower())


def translate(my_text):
    dictionary = {
        "oh really": "orly",
        "seriously": "srsly",
        "uestion": "wesjun",
        "unless": "unles",
        "really": ["rly", "rily", "rilly", "rilley"],
        "you're": ["yore", "yr"],
        "kitten": "kitteh",
        "cture": "kshur",
        "esque": "esk",
        "tious": "shus",
        "thank": ["fank", "tank", "thx", "thnx"],
        "world": ["wurrld", "whirld", "wurld", "wrld"],
        "hello": "oh hai",
        "howdy": "oh hai",
        "kitty": "kitteh",
        "this": "thiz",
        "eady": "eddy",
        "what": ["wut", "whut"],
        "more": "moar",
        "sion": "shun",
        "just": "jus",
        "want": "waants",
        "eese": "eez",
        "ucke": ["ukki", "ukke"],
        "sion": "shun",
        "tion": "shun",
        "like": "liek",
        "love": ["lurv", "lub", "lubs", "luv"],
        "outh": "owf",
        "scio": "shu",
        "ture": "chur",
        "sure": "shur",
        "were": "was",
        "ease": "eez",
        "have": ["has", "hav", "haz"],
        "your": ["yur", "ur", "yore", "yoar"],
        "good": ["gud", "goed", "guud", "gude", "gewd"],
        "ight": "ite",
        "ome": "um",
        "are": ["r", "is", "ar"],
        "you": ["yu", "yoo", "u"],
        "the": "teh",
        "ose": "oze",
        "ead": "edd",
        "eak": "ekk",
        "age": "uj",
        "dog": "dawg",
        "who": "hoo",
        "ese": "eez",
        "too": ["to", "2"],
        "tty": "tteh",
        "thy": "fee",
        "que": "kwe",
        "oth": "udd",
        "ing": ["in", "ins", "ng"],
        "ove": ["oov", "uuv", "uv"],
        "for": ["frr", "4", "fr", "fur", "foar"],
        "i'm": "im",
        "hey": "oh hai",
        "cat": "kitteh",
        "ph": "f",
        "as": "az",
        "my": ["muh", "mah"],
        "er": "r",
        "of": ["ov", "uf"],
        "is": ["ar teh", "ar"],
        "nd": "n",
        "ok": ["k", "kay"],
        "ym": "im",
        "ly": "li"
    }

    for key, value in dictionary.items():
        while key in my_text:
            if isinstance(value, list):
                replacement = random.choice(value)
            else:
                replacement = value
            my_text = my_text.replace(key, replacement, 1)

    return my_text


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)

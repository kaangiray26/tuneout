#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import webbrowser

from flask import (Flask, Response, render_template, request,
                   send_from_directory)
from flask_cors import CORS
from ratelimit import limits, sleep_and_retry

from tuneout.services import Services

app = Flask(__name__, template_folder='docs')
app.services = Services()
CORS(app)

_CALLS = 100
_PERIOD = 60

webbrowser.open('http://127.0.0.1:5000', new=2)


@app.route("/")
@sleep_and_retry
@limits(calls=_CALLS, period=_PERIOD)
def index():
    return render_template("index.html")


@app.route("/music", methods=['POST'])
@sleep_and_retry
@limits(calls=_CALLS, period=_PERIOD)
def music():
    if ('domain' and 'url') not in request.json.keys():
        return Response(status=400)

    response = app.services.get(request.json['domain'], request.json['url'])
    return response
# Assets


@app.route("/assets/<path:path>", methods=["GET"])
@sleep_and_retry
@limits(calls=_CALLS, period=_PERIOD)
def serve_static_files(path):
    return send_from_directory('docs/assets', path)


def main():
    app.run(host='127.0.0.1', port='5000')


if __name__ == "__main__":
    main()

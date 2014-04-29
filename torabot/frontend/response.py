import mimeparse
from flask import request, jsonify


def make_response_content(formats):
    return formats[mimeparse.best_match(formats, request.headers['accept'])]()


def make_response(formats):
    return formats[mimeparse.best_match(formats, request.headers['accept'])]()


def make_ok_response_content():
    return jsonify(dict(ok=True))


def make_ok_response():
    return make_ok_response_content(), 200

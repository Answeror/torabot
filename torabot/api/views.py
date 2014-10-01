import aiohttp
from asyncio import coroutine
from flask import request, jsonify, abort
from . import app
from .. import lang
from ..lang import gist as lang_gist


MIME = {
    'txt': 'text/plain',
    'json': 'application/json',
    'xml': 'text/xml',
    'atom': 'application/atom+xml',
    'rss': 'application/rss+xml',
    'html': 'text/html',
}


@app.route('/source/<gist>.<format>', methods=['GET'])
@coroutine
def source(gist, format):
    if format not in MIME:
        return jsonify({"message": "invalid format"}), 400

    data = yield from lang.make(
        gist=gist,
        args={key: request.args[key] for key in request.args}
    )

    if isinstance(data, int):
        abort(data)

    return data, 200, {'content-type': MIME[format]}


def make_gist_uri(id):
    return 'https://api.github.com/gists/{}'.format(id)


@app.route('/gist/<id>', methods=['GET'])
@coroutine
def gist(id):
    return jsonify((yield from lang_gist.cached_gist(id)))

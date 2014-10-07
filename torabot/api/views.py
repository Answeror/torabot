from logbook import Logger
from ..lang.run import run_json_gist, run_dict
from ..async_web import jsonify
from ..ut.async_request import request as async_request
from .mime import MIME, DEFAULT_FORMAT
from . import app


log = Logger(__name__)


def invalid_format_response(format):
    return jsonify(message='Invalid format: {}'.format(format)), 400, {}


@app.route('/source/{gist}{.format}', method=['GET'])
def source(request, response, gist, format=DEFAULT_FORMAT):
    if format not in MIME:
        return invalid_format_response()

    rv = yield from run_json_gist(
        gist,
        {key: request.args[key][0] for key in request.args}
    )
    return rv, 200, {'content-type': MIME[format]}


@app.route('/make{.format}', method=['POST'])
def make(request, response, format=DEFAULT_FORMAT):
    if format not in MIME:
        return invalid_format_response()

    rv = yield from run_dict((yield from request.json))
    return rv, 200, {'content-type': MIME[format]}


@app.route('/thumb', methods=['GET'])
def thumb(request, response):
    resp = yield from async_request(
        url=request.args['uri'][0],
        method='GET',
        headers={request.args['referer'][0]} if 'referer' in request.args else {}
    )
    data = yield from resp.read()
    return data, 200, {
        key: resp.headers[key] for key in [
            'content-length',
            'content-type',
            'date',
            'expires',
            'last-modified',
        ] if key in resp.headers
    }


@app.route('/ping', method=['GET'])
def ping(request, response):
    return 'pong'

import asyncio
from flask import jsonify, request
from logbook import Logger
from ....lang.run import run_json_gist, run_dict
from ....ut.async_request import request as async_request
from ..mime import MIME, DEFAULT_FORMAT
from .. import bp


log = Logger(__name__)


def invalid_format_response(format):
    return jsonify(message='Invalid format: {}'.format(format)), 400, {}


@bp.route('/source/<gist>', methods=['GET'], defaults={'format': DEFAULT_FORMAT})
@bp.route('/source/<gist>.<format>', methods=['GET'])
def source(gist, format):
    if format not in MIME:
        return invalid_format_response()

    rv = yield from run_json_gist(
        gist,
        {key: request.args[key] for key in request.args}
    )
    return rv, 200, {'content-type': MIME[format]}


@bp.route('/make', methods=['GET'], defaults={'format': DEFAULT_FORMAT})
@bp.route('/make.<format>', methods=['POST'])
def make(format):
    if format not in MIME:
        return invalid_format_response()

    rv = yield from run_dict(request.get_json(force=True))
    return rv, 200, {'content-type': MIME[format]}


@bp.route('/thumb', methods=['GET'])
def thumb():
    resp = yield from async_request(
        url=request.args['uri'],
        method='GET',
        headers={request.args['referer']} if 'referer' in request.args else {}
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


@bp.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@bp.route('/sleep', methods=['GET'])
def sleep():
    yield from asyncio.sleep(1)
    return 'sleep'

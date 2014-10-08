import asyncio
from flask import request, jsonify
from .. import bp
from ....lang.run import run_json_gist


MIME = {
    'txt': 'text/plain',
    'json': 'application/json',
    'xml': 'text/xml',
    'atom': 'application/atom+xml',
    'rss': 'application/rss+xml',
    'html': 'text/html',
}


@bp.route('/source/<gist>', methods=['GET'], defaults={'format': 'txt'})
@bp.route('/source/<gist>.<format>', methods=['GET'])
def source(gist, format):
    if format not in MIME:
        return jsonify({"message": "invalid format"}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    rv = loop.run_until_complete(run_json_gist(
        gist,
        {key: request.args[key] for key in request.args}
    ))
    loop.close()
    return rv, 200, {'content-type': MIME[format]}

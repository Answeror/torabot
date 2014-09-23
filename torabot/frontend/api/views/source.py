from flask import abort, request, jsonify
from .. import bp
from ..ut import make


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

    result = make(
        gist=gist,
        args={key: request.args[key] for key in request.args}
    )

    if isinstance(result, int):
        abort(result)

    return result, 200, {
        'content-type': MIME[format]
    }

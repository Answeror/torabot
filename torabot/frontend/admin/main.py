import json
from logbook import Logger
from flask import render_template, request
from ...core.connection import autoccontext
from ... import db
from . import bp


log = Logger(__name__)


@bp.route('/', methods=['GET'])
def index():
    with autoccontext(commit=False) as conn:
        queries = db.get_sorted_active_queries(conn)
    return render_template('admin/index.html', queries=queries)


@bp.route('/query/<id>/<field>', methods=['GET', 'PUT'])
def query(id, field):
    if request.method == 'GET':
        with autoccontext(commit=False) as conn:
            q = db.get_query_bi_id(id, conn)
        text = q[field]
        if isinstance(text, dict):
            text = json.dumps(text)
        return render_template('jsoneditor.html', text=text)
    if request.method == 'PUT':
        log.info(request.values['text'])
        return ''

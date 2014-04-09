import json
from flask import render_template
from logbook import Logger
from copy import deepcopy
from ..query import get_bangumi, standard_query
from .. import name, bp
from ....ut.bunch import bunchr


log = Logger(__name__)


@bp.route('/bilibili_<hash>.html')
def bilibili_site_verification(hash):
    return bp.send_static_file('bilibili_%s.html' % hash)


def format_query_result(query):
    query = deepcopy(query)
    query.result.query = bunchr(json.loads(standard_query(query.text)[0]))
    return render_template('bilibili/%s.html' % query.result.query.method, query=query)


def format_notice_body(notice):
    return "bilibili: <a href='%s'>%s</a> 更新了" % (
        notice.change.art.uri,
        notice.change.art.title,
    )


def format_bangumi_search():
    return render_template(
        'bilibili/search/bangumi.html',
        bangumi=get_bangumi(),
        kind=name,
    )


def format_user_search():
    return render_template('bilibili/search/user.html', kind=name)


def format_advanced_search(**kargs):
    return {
        'sp': format_bangumi_search,
        'user': format_user_search,
    }[kargs.get('method', 'sp')]()


def format_help_page():
    return render_template('bilibili/help.html')

from flask import render_template
from logbook import Logger
from ..query import get_bangumi
from .. import name


log = Logger(__name__)


def format_query_result(query):
    return render_template('bilibili/sp.html', query=query)


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


def format_advanced_search(**kargs):
    return {
        'bangumi': format_bangumi_search,
    }[kargs.get('method', 'bangumi')]()


def format_help_page():
    return render_template('bilibili/help.html')

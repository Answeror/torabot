import os
from flask import render_template
from logbook import Logger


ROOT = os.path.dirname(os.path.abspath(__file__))

log = Logger(__name__)


def format_query_result(query):
    return render_template('pixiv/list.html', query=query)


def format_notice_body(notice):
    return "pixiv: <a href='%s'>%s</a> 更新了" % (
        notice.change.art.uri,
        notice.change.art.title,
    )


def format_notice_status(notice):
    return {
        'pending': '未发送',
        'sent': '已发送',
    }[notice.status]


def format_query_text(text):
    return text


def format_advanced_search(kind, query):
    return render_template(
        'pixiv/advanced_search.html',
        kind=kind,
        query=query,
    )

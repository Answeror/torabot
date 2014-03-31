from flask import render_template
from .ut import format_change_kind
from .. import name


def format_notice_body(notice):
    return "<a href='%s'>%s</a> %s" % (
        notice.change.art.uri,
        notice.change.art.title,
        format_change_kind(notice.change.kind),
    )


def format_notice_status(notice):
    return {
        'pending': '未发送',
        'sent': '已发送',
    }[notice.status]


def format_query_text(text):
    return text


def format_query_result(query):
    return render_template('tora/list.html', query=query)


def format_advanced_search(**kargs):
    return render_template('tora/advanced_search.html', kind=name)


def format_help_page():
    return render_template('tora/help.html')

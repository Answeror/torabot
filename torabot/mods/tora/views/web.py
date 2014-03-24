import os
from flask import render_template_string, g
from .ut import format_change_kind


ROOT = os.path.dirname(os.path.abspath(__file__))


def format_query_result(query):
    return render_template_string(template('list.html'), query=query)


def template(filename):
    name = 'mod_tora_template'
    s = getattr(g, name, None)
    if s is None:
        with open(os.path.join(ROOT, filename), 'rb') as f:
            s = f.read().decode('utf-8')
        setattr(g, name, s)
    return s


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


def format_advanced_search(kind, query):
    return render_template_string(
        template('advanced_search.html'),
        kind=kind,
        query=query,
    )


def format_help_page():
    return render_template_string(template('help.html'))

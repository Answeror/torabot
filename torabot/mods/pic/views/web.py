from flask import render_template
from .. import Mod


def format_query_result(query):
    return render_template('pic/result.html', query)


def format_notice_body(notice):
    return render_template('pic/notice.html', notice)


def format_advanced_search(**kargs):
    return render_template('pic/search.html')


def format_help_page():
    return render_template('pic/help.html', kind=Mod.name)

from flask import render_template
from ..query import parse as parse_query


def format_query_result(query):
    return {
        'rss': format_rss_result,
    }[parse_query(query.text).method](query)


def format_rss_result(query):
    return render_template('yyets/result/rss.html', query=query)


def format_notice_body(notice):
    return {
        'rss.new': format_rss_notice
    }[notice.change.kind](notice)


def format_rss_notice(notice):
    return render_template('yyets/notice/rss.html', notice=notice)


def format_help_page():
    return render_template('yyets/help.html')

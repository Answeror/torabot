from flask import render_template
from ..query import parse as parse_query
from .. import name


def format_query_result(query):
    return {
        'uri': format_posts,
        'query': format_posts,
    }[parse_query(query.text).method](query)


def format_posts(query):
    return render_template('ehentai/result/posts.html', query=query)


def format_notice_body(notice):
    return {
        'post.new': format_new_post_notice
    }[notice.change.kind](notice)


def format_new_post_notice(notice):
    return render_template('ehentai/notice/new_post.html', notice=notice)


def format_help_page():
    return render_template('ehentai/help.html')


def format_advanced_search(**kargs):
    return render_template('ehentai/search/main.html', kind=name)

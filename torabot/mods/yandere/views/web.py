from flask import render_template
from logbook import Logger
from ..query import parse as parse_query


log = Logger(__name__)


def format_query_result(query):
    return {
        'posts_uri': format_posts_result,
    }[parse_query(query.text).method](query)


def format_posts_result(query):
    return render_template('yandere/result/posts.html', query=query)


def format_new_post_notice(notice):
    return "<span class='label label-primary'>yande.re</span>查询%(sep)s%(query)s%(sep)s更新了<a href='https://yande.re/post/show/%(id)d'>新作品</a>%(sep)s" % dict(
        id=notice.change.post.id,
        query=notice.change.query_text,
        sep='<span class=w-d5em></span>'
    )


def format_notice_body(notice):
    return {
        'post.new': format_new_post_notice,
    }[notice.change.kind](notice)


def format_help_page():
    return render_template('yandere/help.html')

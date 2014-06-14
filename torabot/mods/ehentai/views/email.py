from flask import render_template
import requests
from ....ut.bunch import Bunch


def format_notice_body(notice):
    return {
        'post.new': format_new_post_notice,
    }[notice.change.kind](notice)


def format_new_post_notice(notice):
    return render_template('ehentai/notice/new_post.txt', notice=notice)


def notice_attachments(notice):
    r = requests.get(
        notice.change.post.cover_uri,
        headers=dict(referer='http://g.e-hentai.org/')
    )
    return [Bunch(
        name=notice.change.post.title,
        mime=r.headers['content-type'],
        data=r.content,
    )]

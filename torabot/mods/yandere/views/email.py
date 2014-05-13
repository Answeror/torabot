import requests
from ....ut.bunch import Bunch


def format_new_post_notice(notice):
    return '\n'.join([
        'yande.re',
        '---',
        'query: %(query)s',
        'uri: https://yande.re/post/show/%(id)d',
        'tags: %(tags)s',
    ]) % dict(
        query=notice.change.query_text,
        id=notice.change.post.id,
        tags=notice.change.post.tags,
    )


def format_notice_body(notice):
    return {
        'post.new': format_new_post_notice,
    }[notice.change.kind](notice)


def notice_attachments(notice):
    return {
        'post.new': new_post_notice_attachments,
    }[notice.change.kind](notice)


def new_post_notice_attachments(notice):
    r = requests.get(
        notice.change.post.preview_url,
        headers=dict(referer='https://yande.re/')
    )
    return [Bunch(
        name=notice.change.post.tags,
        mime=r.headers['content-type'],
        data=r.content,
    )]

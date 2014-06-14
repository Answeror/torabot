import requests
from jinja2 import Environment, PackageLoader
from ....ut.bunch import Bunch
from .. import name


env = Environment(loader=PackageLoader('torabot.mods.' + name, 'templates'))


def format_notice_body(notice):
    return {
        'post.new': format_new_post_notice,
    }[notice.change.kind](notice)


def format_new_post_notice(notice):
    return env.get_template('ehentai/notice/new_post.txt').render(notice=notice)


def notice_attachments(notice):
    if not notice.change.post.get('cover_uri', ''):
        return []
    r = requests.get(
        notice.change.post.cover_uri,
        headers=dict(referer='http://g.e-hentai.org/')
    )
    return [Bunch(
        name=notice.change.post.title,
        mime=r.headers['content-type'],
        data=r.content,
    )]

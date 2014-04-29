import requests
from ....ut.bunch import Bunch
from ..translate import translate_mode


def format_user_notice(notice):
    return "pixiv: %(username)s 的 %(title)s 更新了: %(uri)s" % dict(
        uri=notice.change.art.uri,
        title=notice.change.art.title,
        username=notice.change.art.author,
    )


def format_ranking_art(art):
    return '%(username)s 的 %(title)s: %(uri)s' % dict(
        title=art.title,
        uri='http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s' % art.illust_id,
        username=art.user_name,
    )


def format_ranking_notice(notice):
    return '\n'.join([
        "pixiv: %(mode)s 更新了: %(uri)s" % dict(
            uri='http://www.pixiv.net/ranking.php?mode=%s' % notice.change.mode,
            mode=translate_mode(notice.change.mode)
        ),
        '---',
    ] + list(map(format_ranking_art, notice.change.arts)))


def format_notice_body(notice):
    return {
        'new': format_user_notice,
        'user_art.new': format_user_notice,
        'ranking': format_ranking_notice,
    }[notice.change.kind](notice)


def notice_attachments(notice):
    return {
        'new': user_notice_attachments,
        'user_art.new': user_notice_attachments,
        'ranking': ranking_notice_attachments,
    }[notice.change.kind](notice)


def user_notice_attachments(notice):
    r = requests.get(
        notice.change.art.thumbnail_uri,
        headers=dict(referer='http://www.pixiv.net/')
    )
    return [Bunch(
        name=notice.change.art.title,
        mime=r.headers['content-type'],
        data=r.content,
    )]


def ranking_notice_attachments(notice):
    def gen():
        for art in notice.change.arts:
            r = requests.get(
                art.url,
                headers=dict(referer='http://www.pixiv.net/')
            )
            yield Bunch(
                name=art.title,
                mime=r.headers['content-type'],
                data=r.content,
            )
    return list(gen())

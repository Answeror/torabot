import requests
from ....ut.bunch import Bunch


def format_notice_body(notice):
    return "pixiv: %(title)s 更新了: %(uri)s" % dict(
        uri=notice.change.art.uri,
        title=notice.change.art.title,
    )


def notice_attachments(notice):
    r = requests.get(
        notice.change.art.thumbnail_uri,
        headers=dict(referer='http://www.pixiv.net/')
    )
    return [Bunch(
        name=notice.change.art.title,
        mime=r.headers['content-type'],
        data=r.content,
    )]

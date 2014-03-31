def format_notice_body(notice):
    return "pixiv: %(title)s 更新了: %(uri)s" % dict(
        uri=notice.change.art.uri,
        title=notice.change.art.title,
    )

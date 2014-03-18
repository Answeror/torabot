from .ut import format_change_kind


def format_notice(notice):
    return '%(title)s %(change)s: %(uri)s' % dict(
        title=notice.art.title,
        change=format_change_kind(notice.change.kind),
        uri=notice.art.uri,
    )

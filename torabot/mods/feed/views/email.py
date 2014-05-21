def format_notice_body(notice):
    return {
        'feed.new': format_uri_notice,
    }[notice.change.kind](notice)


def format_uri_notice(notice):
    return '%(title)s 更新了: %(link)s' % notice.change.entry

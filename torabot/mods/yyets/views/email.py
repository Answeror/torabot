def format_notice_body(notice):
    return {
        'rss.new': format_rss_notice,
    }[notice.change.kind](notice)


def format_rss_notice(notice):
    return '%(title)s 更新了: %(link)s' % notice.change.art

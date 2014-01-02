import re


def make_change_text(change):
    return {
        change.NEW: '{} 已上架, 链接: {}',
        change.RESERVE: '{} 可预订, 链接: {}',
    }[change.what].format(change.art.title, change.art.uri)


def make_notice_state_string(notice):
    return {
        notice.PENDING: '待发送',
        notice.EATEN: '已发送',
    }[notice.state]


text_web_pattern = re.compile(r'(.*) (已上架|可预订), 链接: (.*)')


def make_notice_text_web(notice):
    m = text_web_pattern.search(notice.text)
    if m is None:
        return notice.text
    return "<a href='{}'>{}</a>{}".format(m.group(3), m.group(1), m.group(2))

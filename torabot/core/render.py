from ..ut.bunch import Bunch
from ..spider.tora import make_query_uri


def render_notice_status(notice):
    return {
        None: '待发送',
        'pending': '待发送',
        'sent': '已发送',
    }[notice.status]


def render_change(old, new):
    return {
        ('other', 'reserve'): '可预定',
        (None, 'other'): '已上架',
        (None, 'reserve'): '已上架',
    }[(old, new)]


def render_notice_text(notice):
    return "<a href='%s'>%s</a> %s" % (
        notice.uri,
        notice.title,
        render_change(notice.old_status, notice.new_status),
    )


def render_notice_html(notice):
    return render_notice_text(notice)


def render_notice_email_body(notice):
    return '%(title)s %(change)s: %(uri)s' % notice


def render_notice(notice):
    notice = Bunch(**notice)
    notice.status_html = render_notice_status(notice)
    notice.change = render_change(notice.old_status, notice.new_status)
    notice.email_body = render_notice_email_body(notice)
    notice.html = render_notice_html(notice)
    return notice


def render_query(query):
    return Bunch(
        uri=make_query_uri(query.text, 0),
        **query
    )

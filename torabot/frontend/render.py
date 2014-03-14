def render_notice_status(notice):
    return {
        None: '待发送',
        'pending': '待发送',
        'sent': '已发送',
    }[notice.status]


def render_notice_text(notice):
    status = {
        ('other', 'reserve'): '可预定',
        (None, 'other'): '已上架',
        (None, 'reserve'): '已上架',
    }[(notice.old_status, notice.new_status)]
    return "<a href='%s'>%s</a>%s" % (
        notice.uri,
        notice.title,
        status,
    )

from urllib.parse import quote


def format_notice_body(notice):
    return {
        'sp': format_sp_notice_body,
        'user_new_post': format_user_notice_body,
    }[notice.change.kind](notice)


def format_sp_notice_body(notice):
    return "bilibili: %(title)s 更新至第%(n)d话: %(uri)s" % dict(
        title=notice.change.sp.title,
        n=notice.change.sp.bgmcount,
        uri=quote('http://www.bilibili.tv/sp/' + notice.change.sp.title),
    )


def format_user_notice_body(notice):
    return "bilibili: 新投稿 %(title)s: %(uri)s" % dict(
        title=notice.change.post.title,
        uri=notice.change.post.uri,
    )

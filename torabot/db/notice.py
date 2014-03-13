from ..ut.bunch import Bunch


def get_notice_bi_user_id(conn, user_id):
    result = conn.execute((
        'select * from notice '
        'where user_id = %s '
    ), (user_id,))
    return [Bunch(**row) for row in result.fetchall()]

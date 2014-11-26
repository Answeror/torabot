from asyncio import coroutine
from nose.tools import assert_equal
from ...ut.bunch import bunchr
from ...ut.return_list import return_list
from . import bilibili


@coroutine
@return_list
def changes(old, new):
    if old:
        assert_equal(
            bilibili._query_method_from_result(old),
            bilibili._query_method_from_result(new)
        )
    yield from {
        'bangumi': bangumi_changes,
        'sp': sp_changes,
        'user': user_changes,
        'username': user_changes,
        'query': query_changes,
    }[bilibili._query_method_from_result(new)](bunchr(old), bunchr(new))


def bangumi_changes(old, new):
    return []


def sp_changes(old, new):
    if not old:
        yield bunchr(kind='sp_new', sp=new.sp)
        return
    if not new or not new.sp:
        return
    if (
        not old.sp or
        new.sp.bgmcount != old.sp.bgmcount or
        new.sp.lastupdate != old.sp.lastupdate
    ):
        yield bunchr(kind='sp_update', sp=new.sp)


def user_changes(old, new):
    return post_changes('user_new_post', old, new)


def query_changes(old, new):
    return post_changes('query_new_post', old, new)


def post_changes(kind_prefix, old, new):
    oldmap = {post.uri: post for post in getattr(old, 'posts', [])}
    for post in new.get('posts', []):
        if post.get('uri') not in oldmap:
            yield bunchr(kind='user_new_post', post=post)


__all__ = ['changes']

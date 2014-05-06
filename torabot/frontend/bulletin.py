from ..core.redis import redis


def get_bulletin_text():
    return (redis.get('torabot:bulletin:text') or b'').decode('utf-8')


def set_bulletin_text(value):
    redis.set('torabot:bulletin:text', (value or '').encode('utf-8'))


def get_bulletin_type():
    return (redis.get('torabot:bulletin:type') or b'').decode('utf-8')


def set_bulletin_type(value):
    redis.set('torabot:bulletin:type', (value or '').encode('utf-8'))

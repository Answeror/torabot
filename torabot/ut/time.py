from datetime import datetime


TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
TIME_DISPLAY_FORMAT = '%Y-%m-%d %H:%M:%S'


def tokyo_to_utc(dt):
    import pytz
    local = pytz.timezone('Asia/Tokyo')
    local_dt = local.localize(dt, is_dst=None)
    return local_dt.astimezone(pytz.utc).replace(tzinfo=None)


def utc_to_tokyo(dt):
    import pytz
    return dt.astimezone(pytz.timezone('Asia/Tokyo')).replace(tzinfo=None)


def _utcnow():
    return datetime.utcnow()


def utcnow():
    return _utcnow()

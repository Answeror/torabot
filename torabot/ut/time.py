import pytz
from datetime import datetime


def tokyo_to_utc(dt):
    local = pytz.timezone('Asia/Tokyo')
    local_dt = local.localize(dt, is_dst=None)
    return local_dt.astimezone(pytz.utc).replace(tzinfo=None)


def utc_to_tokyo(dt):
    return dt.astimezone(pytz.timezone('Asia/Tokyo')).replace(tzinfo=None)


def _utcnow():
    return datetime.utcnow()


def utcnow():
    return _utcnow()

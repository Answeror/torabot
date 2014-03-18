from ...ut.bunch import Bunch


def changes(old, new):
    oldmap = {art.uri for art in getattr(old, 'arts', [])}
    for art in new.arts:
        if art.uri not in oldmap:
            yield Bunch(kind='new', art=art)
        elif (oldmap[art.uri].status, art.status) in noticeable():
            yield Bunch(kind='notice', art=art)


def noticeable():
    return [
        (None, 'reserve'),
        ('other', 'reserve'),
    ]

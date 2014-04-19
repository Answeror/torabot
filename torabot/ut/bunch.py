from nose.tools import assert_equal


class Bunch(dict):

    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


def bunchr(*args, **kargs):
    if args:
        assert_equal(len(args), 1)
        assert not kargs
        d = args[0]
    else:
        d = kargs
    if isinstance(d, dict):
        return Bunch(**{key: bunchr(value) for key, value in d.items()})
    if isinstance(d, list):
        return [bunchr(e) for e in d]
    return d


def bunchset(d, **kargs):
    d = bunchr(**d)
    d.update(kargs)
    return d


def bunchdel(d, *names):
    d = bunchr(**d)
    for name in names:
        del d[name]
    return d

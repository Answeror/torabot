from nose.tools import assert_equal


class Bunch(dict):

    def __getattr__(self, key):
        return self[key]

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

def ignore_none(f):
    def inner(arg):
        if arg is not None:
            return f(arg)
    return inner

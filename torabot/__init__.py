def make(*args, **kargs):
    from .app import App
    return App(__name__, *args, **kargs)

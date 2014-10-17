from logbook.compat import redirect_logging
redirect_logging()


from torabot.api import app
assert app

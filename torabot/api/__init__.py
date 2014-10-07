from ..async_web import App


app = App(__name__)


from . import views
assert views

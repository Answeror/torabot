from uuid import uuid4
from flask import current_app, Blueprint, _app_ctx_stack
from threading import Lock
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from asyncio import coroutine, iscoroutine, get_event_loop
from .bunch import Bunch


class Facade(object):

    def __init__(self):
        self.__init_parts = []
        self.__executor_lock = Lock()

    @property
    def name(self):
        value = getattr(self, '_name', None)
        if value is None:
            self._name = value = str(uuid4())
        return value

    @property
    def state(self):
        return current_app.parts[self.name]

    def init_app(self, app, loop=None):
        app.parts[self.name] = Bunch()

        if loop is None:
            loop = get_event_loop()

        for part in self.__init_parts:
            if iscoroutine(part):
                loop.run_until_complete(part(app))
            else:
                part(app)

        app.config.setdefault('TORABOT_CONCURRENCY', 2 * cpu_count())

    def initializer(self, func):
        self.__init_parts.append(func)
        return func

    def interface(self, func):
        setattr(self, func.__name__, func)
        return func

    def setattr(self, attr):
        setattr(self, attr.__name__, attr)
        return attr

    @property
    def executor(self):
        with self.__executor_lock:
            value = self.state.get('executor')
            if value is None:
                self.state.executor = value = ThreadPoolExecutor(
                    max_workers=current_app.config['TORABOT_CONCURRENCY']
                )
            return value

    @coroutine
    def run_in_executor(self, func, *args, **kargs):
        app_context = _app_ctx_stack.top

        def wrapped():
            if app_context is None:
                return func(*args, **kargs)
            with app_context:
                return func(*args, **kargs)

        return (yield from current_app.loop.run_in_executor(
            self.executor,
            wrapped
        ))


class BlueprintField(object):

    def __init__(self, import_name):
        self.import_name = import_name

    def __get__(self, obj, cls):
        if cls is None:
            cls = type(obj)
        name = '_blueprint'
        value = getattr(self, name, None)
        if value is None:
            value = Blueprint(
                obj.name,
                self.import_name,
                static_folder='static',
                template_folder='templates',
                static_url_path='/%s/static' % obj.name
            )
            setattr(cls, name, value)
        return value


def blueprint_mixin(import_name):
    class BlueprintMixin(object):

        blueprint = BlueprintField(import_name)

        def init_app(self, app):
            super().init_app(app)
            app.register_blueprint(self.blueprint)

    return BlueprintMixin

import jsonpickle
from celery import Celery
from functools import wraps
from asyncio import coroutine
from .app_mixins import RedisPubMixin


PUBSUB_CHANNEL_TEMPLATE = 'torabot:task:{}'


class App(RedisPubMixin, Celery):

    def _arg1_type_error(self):
        raise TypeError('argument 1 to @task() must be a callable')

    def _args_error(self, args, kargs):
        raise TypeError(
            '@task() takes exactly 1 argument ({0} given)'.format(
                sum([len(args), len(kargs)])
            )
        )

    def task(self, *args, **kargs):
        def wrap(f):
            @wraps(f)
            def g(*args, **kargs):
                with self.redispub.applicationbound():
                    return f(*args, **kargs)
            return g

        if len(args) == 1:
            if callable(args[0]):
                return super(App, self).task(wrap(args[0]))
            self._arg1_type_error()

        if args:
            self._args_error()

        return (lambda f: super(App, self).task(**kargs)(wrap(f)))

    def async_task(self, *args, **kargs):
        def wrap(f):
            @wraps(f)
            def g(self, *args, **kargs):
                from .ut.local import local
                ret = f(*args, **kargs)
                local.redis.publish(
                    PUBSUB_CHANNEL_TEMPLATE.format(self.request.id),
                    jsonpickle.encode(ret)
                )
            return g

        def yawrap(task):
            @coroutine
            @wraps(task)
            def g(*args, **kargs):
                from .ut.async_local import local
                redis = yield from local.redis
                sub = yield from redis.start_subscribe()
                r = task.delay(*args, **kargs)
                yield from sub.subscribe([PUBSUB_CHANNEL_TEMPLATE.format(r.id)])
                return jsonpickle.decode((yield from sub.next_published()).value)
            return g

        if len(args) == 1:
            if callable(args[0]):
                return yawrap(self.task(bind=True)(wrap(args[0])))
            self._arg1_type_error()

        if args:
            self._args_error()

        return (lambda f: yawrap(self.task(bind=True, **kargs)(wrap(f))))


app = App('torabot', include=['torabot.lang.tasks'])
app.config_from_object('torabot.celery_conf')


@app.task
def sync_all():
    from torabot import tasks
    tasks.sync_all(app.conf)


@app.task
def notice_all():
    from torabot import tasks
    tasks.notice_all(app.conf)


@app.task
def log_to_file():
    from torabot import tasks
    tasks.log_to_file()


@app.task
def tell_admin_safe(*args, **kargs):
    from torabot import tasks
    return tasks.tell_admin_safe(*args, **kargs)


@app.task
def del_inactive_queries():
    from torabot import tasks
    return tasks.del_inactive_queries()


@app.task
def del_old_changes():
    from torabot import tasks
    return tasks.del_old_changes()


if __name__ == '__main__':
    app.start()

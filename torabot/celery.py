import jsonpickle
from celery import Celery as Base
from functools import wraps
from asyncio import coroutine
from .app_mixins import RedisPubMixin
from .app import App


PUBSUB_CHANNEL_TEMPLATE = 'torabot:task:{}'


class Celery(RedisPubMixin, Base):

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
                    with app.app_context():
                        return f(*args, **kargs)
            return g

        if len(args) == 1:
            if callable(args[0]):
                return super(Celery, self).task(wrap(args[0]))
            self._arg1_type_error()

        if args:
            self._args_error()

        return (lambda f: super(Celery, self).task(**kargs)(wrap(f)))

    def async_task(self, *args, **kargs):
        def wrap(f):
            @wraps(f)
            def g(self, *args, **kargs):
                from .ut.redis import redis
                ret = f(*args, **kargs)
                with app.app_context():
                    redis.sync_publish(
                        PUBSUB_CHANNEL_TEMPLATE.format(self.request.id),
                        jsonpickle.encode(ret)
                    )
            return g

        def yawrap(task):
            @coroutine
            @wraps(task)
            def g(*args, **kargs):
                from .ut.redis import redis
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


celery = Celery(__name__, include=[
    'torabot.ut.xml'
])
app = App(__name__)


@celery.task
def sync_all():
    from torabot import tasks
    tasks.sync_all(celery.conf)


@celery.task
def notice_all():
    from torabot import tasks
    tasks.notice_all(celery.conf)


@celery.task
def log_to_file():
    from torabot import tasks
    tasks.log_to_file()


@celery.task
def tell_admin_safe(*args, **kargs):
    from torabot import tasks
    return tasks.tell_admin_safe(*args, **kargs)


@celery.task
def del_inactive_queries():
    from torabot import tasks
    return tasks.del_inactive_queries()


@celery.task
def del_old_changes():
    from torabot import tasks
    return tasks.del_old_changes()


if __name__ == '__main__':
    celery.start()

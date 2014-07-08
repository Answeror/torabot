from celery import Celery
from functools import wraps
from .app_mixins import RedisPubMixin


class App(RedisPubMixin, Celery):

    def torabot_task(self, f):
        @wraps(f)
        def inner(*args, **kargs):
            with self.redispub.applicationbound():
                return f(*args, **kargs)
        return self.task(inner)


app = App('torabot')

try:
    import toraconf
    assert toraconf
    app.config_from_object('toraconf')
except:
    app.config_from_object('torabot.conf')


@app.torabot_task
def sync_all():
    from torabot import tasks
    tasks.sync_all(app.conf)


@app.torabot_task
def notice_all():
    from torabot import tasks
    tasks.notice_all(app.conf)


@app.torabot_task
def log_to_file():
    from torabot import tasks
    tasks.log_to_file()


@app.torabot_task
def tell_admin_safe(*args, **kargs):
    from torabot import tasks
    return tasks.tell_admin_safe(*args, **kargs)


@app.torabot_task
def make_source(files, conf):
    from torabot import tasks
    return tasks.make_source(files, conf)


@app.torabot_task
def del_inactive_queries():
    from torabot import tasks
    return tasks.del_inactive_queries()


@app.torabot_task
def del_old_changes():
    from torabot import tasks
    return tasks.del_old_changes()


if __name__ == '__main__':
    app.start()

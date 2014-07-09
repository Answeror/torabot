from celery.concurrency.base import apply_target, BasePool
from concurrent.futures import ThreadPoolExecutor as Ex


__all__ = ['TaskPool']


class TaskPool(BasePool):

    def __init__(self, *args, **kwargs):
        super(TaskPool, self).__init__(*args, **kwargs)

    def on_start(self):
        self.ex = Ex(self.limit)

    def on_stop(self):
        self.ex.shutdown(True)

    def on_apply(self, target, args=None, kwargs=None, callback=None, accept_callback=None, **_):
        return self.ex.submit(apply_target, target, args, kwargs, callback, accept_callback)

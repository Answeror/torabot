import logbook.queues
import logbook
import json
from flask import current_app
from .redis import redis


class RedisPub(logbook.queues.RedisHandler):

    def __init__(self, level=logbook.DEBUG, bubble=True):
        super(RedisPub, self).__init__(
            key='torabot:log',
            level=level,
            bubble=bubble
        )
        self.disable_buffering()

    def export_record(self, record):
        """Exports the record into a dictionary ready for JSON dumping."""
        return record.to_dict(json_safe=True)

    def emit(self, record):
        with self.lock:
            self.queue.append(
                json.dumps(self.export_record(record)).encode("utf-8")
            )
            if len(self.queue) == self.flush_threshold:
                self._flush_buffer()


class RedisSub(logbook.queues.SubscriberBase):

    key = 'torabot:log'

    def recv(self, timeout=None):
        if timeout is None:
            rv = current_app.loop.run_until_complete(redis.blpop(self.key))
            value = rv[1]
        elif timeout == 0:
            value = current_app.loop.run_until_complete(redis.lpop(self.key))
        else:
            rv = current_app.loop.run_until_complete(redis.blpop(self.key))
            value = None if rv is None else rv[1]

        if value is None:
            return None

        d = json.loads(value.decode('utf-8'))
        return logbook.LogRecord.from_dict(d)

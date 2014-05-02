from scrapy_redis import connection
from scrapy import signals, log
from scrapy.spider import Spider
from scrapy.exceptions import DontCloseSpider
from time import time


class RedisMixin(object):
    """Mixin class to implement reading urls from a redis queue."""

    life = None

    @property
    def start_time(self):
        name = '_start_time'
        value = getattr(self, name, None)
        if value is None:
            value = time()
            setattr(self, name, value)
        return value

    @property
    def redis_key(self):
        return 'torabot:spy:' + self.name

    def next_requests(self):
        """Returns a request to be scheduled or none."""
        query = self.server.lpop(self.redis_key)
        if query:
            query = decode(query)
            log.msg(u'got query %s' % query, level=log.INFO)
            for req in self.make_requests_from_query(query):
                yield req

    def make_requests_from_query(self, query):
        req = self.make_request_from_query(query)
        if req:
            yield req

    def setup_redis(self):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if not self.redis_key:
            self.redis_key = '%s:start_urls' % self.name

        self.server = connection.from_settings(self.crawler.settings)
        # idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        self.crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
        log.msg("Reading URLs from redis list '%s'" % self.redis_key, level=log.INFO)

    def schedule_next_request(self):
        """Schedules a request if available"""
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def schedule_rest_requests(self):
        while True:
            reqs = list(self.next_requests())
            if not reqs:
                break
            for req in reqs:
                self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        self.schedule_rest_requests()
        if self.life is None or (time() - self.start_time < self.life):
            raise DontCloseSpider

    def item_scraped(self, *args, **kwargs):
        """Avoids waiting for the spider to  idle before scheduling the next request"""
        self.schedule_rest_requests()


class RedisSpider(RedisMixin, Spider):
    """Spider that reads urls from redis queue when idle."""

    def __init__(self, life=None, *args, **kargs):
        super(RedisSpider, self).__init__(*args, **kargs)
        self.life = None if life is None else float(life)

    def set_crawler(self, crawler):
        super(RedisSpider, self).set_crawler(crawler)
        self.setup_redis()


def decode(query):
    return query.decode('utf-8') if isinstance(query, str) else query

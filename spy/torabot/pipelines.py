# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_redis.pipelines import RedisPipeline
from scrapy import log
from .items import Result


class SpyPipeline(object):
    def process_item(self, item, spider):
        return item


class Output(RedisPipeline):

    def item_key(self, item, spider):
        """Returns redis key based on given spider"""
        return "torabot:spy:%s:%s:items" % (spider.name, spider.id)

    def process_item(self, item, spider):
        try:
            return RedisPipeline.process_item(self, item, spider)
        finally:
            self.exist_item = True

    def close_spider(self, spider):
        if not getattr(self, 'exist_item', False):
            log.msg('no item processed, push failed result', level=log.INFO)
            self.process_item(Result(ok=False), spider)

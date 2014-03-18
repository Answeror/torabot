# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_redis.pipelines import RedisPipeline


class SpyPipeline(object):
    def process_item(self, item, spider):
        return item


class Output(RedisPipeline):

    def item_key(self, item, spider):
        """Returns redis key based on given spider"""
        return "torabot:spy:%s:%s:items" % (spider.name, spider.id)

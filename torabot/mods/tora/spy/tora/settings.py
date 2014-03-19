# Scrapy settings for tora project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tora'

SPIDER_MODULES = ['tora.spiders']
NEWSPIDER_MODULE = 'tora.spiders'

ITEM_PIPELINES = {
    'torabot.spy.pipelines.Output': 42,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    'torabot.spy.middlewares.RotateUserAgentMiddleware': 400,
    'tora.middlewares.Retry': 500,
}

#To make RotateUserAgentMiddleware enable.
USER_AGENT = ''
HTTPCACHE_ENABLED = True
DNSCACHE_ENABLED = True
DOWNLOAD_DELAY = 0.1
AUTOTHROTTLE_ENABLED = True

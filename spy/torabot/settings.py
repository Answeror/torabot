# Scrapy settings for torabot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'torabot'

SPIDER_MODULES = ['torabot.spiders']
NEWSPIDER_MODULE = 'torabot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'torabot (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'torabot.pipelines.Output': 42,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    'torabot.middlewares.RotateUserAgentMiddleware': 400,
    'torabot.middlewares.ToraRetry': 500,
}

#To make RotateUserAgentMiddleware enable.
USER_AGENT = ''
DOWNLOAD_DELAY = 0.1
AUTOTHROTTLE_ENABLED = True

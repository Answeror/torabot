# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from torabot.mods.booru.spiders import Booru


class Danbooru(Booru):

    name = 'danbooru'

    def __init__(self, life=60, *args, **kargs):
        super(Danbooru, self).__init__(
            *args,
            life=life,
            posts_url='http://danbooru.donmai.us/posts'
        )

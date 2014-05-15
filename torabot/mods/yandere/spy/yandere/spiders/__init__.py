# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from torabot.mods.booru.spiders import Booru


class Yandere(Booru):

    name = 'yandere'

    def __init__(self, life=60, *args, **kargs):
        super(Yandere, self).__init__(
            *args,
            life=life,
            posts_url='https://yande.re/post'
        )

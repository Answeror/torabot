from setuptools import setup, find_packages


setup(
    name='torabot',
    version='0.1.0',
    packages=find_packages(),

    entry_points={
        'torabot.mods': [
            'tora = torabot.mods.tora:Tora',
            'pixiv = torabot.mods.pixiv:Pixiv',
            'bilibili = torabot.mods.bilibili:Bilibili',
            'yyets = torabot.mods.yyets:Yyets',
            'yandere = torabot.mods.yandere:Yandere',
            'danbooru = torabot.mods.danbooru:Danbooru',
            'feed = torabot.mods.feed:Feed',
            'ehentai = torabot.mods.ehentai:Ehentai',
            'gist = torabot.mods.gist:Gist',
        ]
    },
)

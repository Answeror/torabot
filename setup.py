from setuptools import setup, find_packages


setup(
    name='torabot',
    version='0.1.0',
    packages=find_packages(),

    entry_points={
        'torabot.mods': [
            'tora = torabot.mods.tora:Tora',
        ]
    },
)

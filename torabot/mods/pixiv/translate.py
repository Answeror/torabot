from collections import OrderedDict


def modemap():
    return OrderedDict([
        ('daily', '本日'),
        ('daily_r18', '本日(R18)'),
        ('weekly', '本周'),
        ('weekly_r18', '本周(R18)'),
        ('monthly', '本月'),
        ('rookie', '新人'),
        ('original', '原创'),
        ('male', '男性向'),
        ('male_r18', '男性向(R18)'),
        ('female', '女性向'),
        ('female_r18', '女性向(R18)'),
    ])


def translate_mode(mode):
    return modemap()[mode]

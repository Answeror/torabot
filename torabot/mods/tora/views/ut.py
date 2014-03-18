def format_change_kind(kind):
    return {
        ('new'): '已上架',
        ('notice'): '可预定',
    }[kind]

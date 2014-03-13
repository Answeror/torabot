def check_new(old, new):
    def gen():
        uris = {art['uri'] for art in old}
        for art in new:
            if art['uri'] not in uris:
                yield art

    return list(gen())


def check_reserve(old, new):
    def gen():
        uris = {art['uri'] for art in old if not art['reserve']}
        for art in new:
            if art['uri'] not in uris or art['reserve']:
                yield art

    return list(gen())

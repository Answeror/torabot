class G(object):

    def __init__(self):
        self.d = {}

    def __getattr__(self, key):
        return super(G, self).__getattr__(key) if key == 'd' else self.d[key]

    def __setattr__(self, key, value):
        if key == 'd':
            super(G, self).__setattr__(key, value)
        else:
            self.d[key] = value


g = G()

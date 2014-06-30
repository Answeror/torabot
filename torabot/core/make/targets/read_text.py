from .read import Target as Read


class Target(Read):

    def __call__(self, name):
        return super(Target, self).__call__(name, 'text')

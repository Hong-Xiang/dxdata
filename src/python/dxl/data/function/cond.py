from dxl.data.core import function, Function

__all__ = ['is_decay', 'AllIsInstance']


@function
def is_decay(l):
    return all([x >= y for x, y in zip(l, l[1:])])


class AllIsInstance(Function):
    def __init__(self, target_type):
        self.target_type = target_type

    def __call__(self, it):
        return all(map(lambda o: isinstance(o, self.target_type), it))

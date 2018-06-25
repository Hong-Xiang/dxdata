from dxl.data.core import function, Function

__all__ = ['is_decay', 'AllIsInstance', 'MapIf', 'Always']


@function
def is_decay(l):
    return all([x >= y for x, y in zip(l, l[1:])])


class AllIsInstance(Function):
    def __init__(self, target_type):
        self.target_type = target_type

    def __call__(self, it):
        return all(map(lambda o: isinstance(o, self.target_type), it))


class MapIf(Function):
    def __init__(self, cond, f):
        self.cond = cond
        self.f = f

    def __call__(self, x):
        if self.cond(x):
            return self.f(x)
        else:
            return x


class Always(Function):
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value


class Switch(Function):
    def __init__(self, cond, f_true, f_false):
        self.cond = cond
        self.f_true = f_true
        self.f_false = f_false

    def __call__(self, x):
        if self.cond(x):
            return self.f_true(x)
        else:
            return self.f_false(x)


@function
def is_none(x):
    return x is None

from functools import partial
from itertools import dropwhile
from dxl.data import ItertoolsIterable, ChainableIterable


def test_itertools_iterable():
    it = ItertoolsIterable(range(10), partial(dropwhile, lambda x: x < 3))
    assert list(it) + list(it) == list(range(3, 10)) * 2


def test_chainable_iterable():
    it = range(10)
    it = ChainableIterable(it, lambda x: x + 11)
    assert list(it) + list(it) == list(range(11, 21)) * 2

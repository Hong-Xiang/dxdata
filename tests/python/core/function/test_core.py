import pytest
from dxl.data.core.function.core import *


@pytest.fixture
def call_spy():
    class CallSpy:
        def __init__(self):
            self.nb_called = 0

        def __call__(self):
            self.nb_called += 1

    return CallSpy()


def test_wrapped_function(call_spy):
    f = function(call_spy)
    assert isinstance(f, Function)
    assert call_spy.nb_called == 0
    f()
    assert call_spy.nb_called == 1


def test_on_iterator():
    add = lambda x, v: x + v

    def gen():
        for i in range(10):
            yield i

    add_to_iterator = OnIterator(add)

    it = add_to_iterator(gen(), 5)

    results = [x for x in it]
    assert results == list(range(5, 15))




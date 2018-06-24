from dxl.data.core.function.nest import *

import pytest


@pytest.fixture
def gen5():
    def foo():
        for i in range(5):
            yield i

    return foo()


def test_take_list():
    r = Take(2)([1, 2, 3, 4])
    assert r == [1, 2]


def test_take_iter(gen5):
    r = Take(2)(gen5)
    assert r == [0, 1]


def test_take_iter_multiple_times(gen5):
    r = Take(2)(gen5)
    r = Take(2)(gen5)
    assert r == [2, 3]
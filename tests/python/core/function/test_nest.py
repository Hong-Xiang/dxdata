from dxl.data.core.function.nest import *

import pytest
import typing
from collections import namedtuple


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


def test_nest_map_of_on_list():
    f = NestMapOf(lambda x: x + 1)
    assert f([1, 2, 3]) == [2, 3, 4]


def test_nest_map_of_on_tuple():
    f = NestMapOf(lambda x: x + 1)
    assert f((1, 2, 3)) == (2, 3, 4)


def test_nest_map_of_on_dict():
    f = NestMapOf(lambda x: x + 1)
    assert f({'x': 1, 'y': 2}) == {'x': 2, 'y': 3}


def test_head():
    assert head([1, 2, 3]) == 1


def test_head_iter(gen5):
    assert head(gen5) == 0


def test_select_map_of_on_dict():
    d = {'x': 1, 'y': 2}
    f = MapByNameOf('x', lambda x: x + 3)
    assert f(d) == {'x': 4, 'y': 2}


def test_select_map_of_on_typing_named_tuple():
    class C(typing.NamedTuple):
        x: int
        y: int
    f = MapByNameOf('x', lambda x: x + 3)
    assert f(C(1, 2)) == C(4, 2)


def test_select_map_of_on_named_tuple():
    C = namedtuple('C', ['x', 'y'])
    f = MapByNameOf('x', lambda x: x + 3)
    assert f(C(1, 2)) == C(4, 2)


def test_swap():
    assert Swap(1, 2)([4, 5, 6]) == [4, 6, 5]

from dxl.data.core.function.func import *
import pytest


@pytest.fixture
def multi_impls():
    return {int: lambda x: x + 1, str: lambda s: s + '1'}


def test_multi_methods_function(multi_impls):
    f = MultiMethodsFunction(multi_impls, type)
    assert f(1) == 2
    assert f('1') == '11'


def test_head_arg():
    assert head_arg(0) == 0


def test_head_arg():
    assert head_arg(0, 1) == 0


def test_multi_methods_by_type_of_first_arg(multi_impls):
    def foo(*args, **kwags):
        return args[0] + 1

    multi_impls.update({int: foo})
    f = MultiMethodsByTypeOfFirstArg(multi_impls)
    assert f(1) == 2
    assert f(1, 2) == 2
    assert f('1') == '11'

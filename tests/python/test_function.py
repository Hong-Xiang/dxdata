from dxl.data import Function
def test_currying():
    def foo_(a, b, c):
        return a + b + c
    foo = Function(foo_) 
    f1 = foo(1)
    f2 = f1(2)
    v = f2(3)
    assert v == 6
    assert f2(4) == 7
    assert f1(7, 9) == 17
    assert foo(1, 4, 6) == 11 
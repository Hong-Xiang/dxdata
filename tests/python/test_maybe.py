from dxl.data import Maybe


def test_maybe():
    def deposit(m):
        def kernel(b):
            return Maybe(b+m)
        return kernel

    def withdraw(m):
        def kernel(b):
            if b < m:
                return Maybe(None)
            return Maybe(b-m)
        return kernel
    b = Maybe(30)
    assert (b >> deposit(10)).join() == 40
    assert (b >> deposit(10) >> deposit(20)
            >> withdraw(50) >> deposit(60)).join() == 70
    assert (b >> deposit(10) >> withdraw(50) >> deposit(60)).join() is None

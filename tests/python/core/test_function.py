from dxl.data.core.function import *


class TestMultiDispatchByArgs:
    def test_len_of_key_equals_one(self):
        class MultiPatchAdd(MultiDispatchByArgs):
            def __init__(self):
                super().__init__({int: self._int, str: self._str})

            def _int(self, x):
                return x + 1

            def _str(self, x):
                return x + '1'

        foo = MultiPatchAdd()
        assert foo(1) == 2
        assert foo('1') == '11'

    def test_auto_search_impl(self):
        class MultiPatchAdd(MultiDispatchByArgs):
            def __init__(self):
                super().__init__(len_of_key=1)

            def _int(self, x):
                return x + 1

            def _str(self, x):
                return x + '1'

        foo = MultiPatchAdd()
        assert foo(1) == 2
        assert foo('1') == '11'

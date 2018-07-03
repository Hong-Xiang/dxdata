from dxl.data.function import Function
from dxl.data.core.columns import ColumnsWithIndex, Columns
from typing import Iterable, Optional, List


class _ColumnsPartition(ColumnsWithIndex):
    def __init__(self, source_columns, indices, capacity=None):
        super().__init__(source_columns.dataclass)
        if capacity is None:
            capacity = len(indices)
        self._capacity = capacity
        self._indices = indices
        self.source_columns = source_columns

    @property
    def capacity(self):
        return self._capacity

    @property
    def shapes(self):
        return self.source_columns.shapes

    @property
    def dtypes(self):
        return self.source_columns.dtypes

    def __getitem__(self, index):
        return self.source_columns[self._indices[index]]

    def __iter__(self):
        def it():
            for i in self._indices:
                yield self.source_columns[i]
        return it()


class Partition(Function):
    def __call__(self, c: ColumnsWithIndex):
        return _ColumnsPartition(c, self.indices(c), self.capacity(c))

    def indices(self, columns) -> Iterable:
        raise NotImplementedError

    def capacity(self, columns) -> int:
        raise NotImplementedError


class CrossValidatePartition(Partition):
    def __init__(self, nb_blocks: int, in_blocks: List[int]):
        self.nb_blocks = nb_blocks
        self.in_blocks = in_blocks

    def indices(self, columns) -> Iterable:
        step = self.capacity(columns) // self.nb_blocks
        result = []
        for i in self.in_blocks:
            result += list(range(i * step, (i + 1) * step))
        return result

    def capacity(self, columns) -> int:
        return columns.capacity // self.nb_blocks * len(self.in_blocks)


class Train80Partitioner(CrossValidatePartition):
    def __init__(self, is_train):
        nb_blocks, nb_train = 10, 8
        if is_train:
            in_blocks = range(nb_train)
        else:
            in_blocks = range(nb_train, nb_blocks)
        super().__init__(nb_blocks, in_blocks)

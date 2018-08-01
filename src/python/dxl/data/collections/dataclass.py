import collections.abc
from typing import Sequence, TypeVar
from dxl.data import Functor, Monoid, List


def batched(f):
    return f


a = TypeVar('a')


class DataCollection(Sequence[a], Functor[a], Monoid[a]):
    pass


class DataList(DataCollection[a], List[a]):
    def __init__(self, dataclass, data):
        super().__init__(data)
        self.dataclass = dataclass

    def fmap(self, f):
        result = [f(x) for x in self.join()]
        return DataList(type(result), result)

    def filter(self, f):
        return DataList(self.dataclass, [x for x in self.join() if f(x)])


class DataArray(Sequence[a], Functor[a]):
    def __init__(self, dataclass, data):
        self.data = data
        self.dataclass = dataclass

    def fmap(self, f):
        result = f((self.join()))
        return DataArray(type(result), result)

    def __len__(self):
        return self.data.shape[0]

    def filter(self, f):
        result = self.join()[f(self.join())]
        return DataArray(self.dataclass, result)

    def __getitem__(self, s):
        if isinstance(s, int):
            return self.join()[s]
        else:
            return self.fmap(lambda d: d[s])

    def join(self):
        return self.data

    def __repr__(self):
        return f"<DataArray({self.dataclass}, {self.join()})>"




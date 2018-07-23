from typing import Generic, TypeVar, NamedTuple, Sequence
from abc import ABCMeta, abstractproperty, abstractmethod
from .control import Functor
from .monoid import Monoid

a = TypeVar('a')

class Table(Functor[a], Monoid[a], Sequence[a]):
    """
    An unified table access of PyTable/pandas, etc.

    t[0]: 0-th row
    t[0:5] -> Table: [0:5] rows.

    __iter__(self): row iterator

    fmap :: Table -> Table

    """

    def __getitem__(self, labels, columns=None):
        if isinstance(labels, int) and (isinstance(labels, slice) and isinstance(labels.start, int)):
            return self.iloc[labels]

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def iloc(self, l):
        pass

    @abstractproperty
    def nb_rows(self):
        pass
    
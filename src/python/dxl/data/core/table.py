from abc import ABCMeta, abstractproperty, abstractmethod


class Table(metaclass=ABCMeta):
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
    def fmap(self, f):
        pass

    @abstractproperty
    def iloc(self):
        pass

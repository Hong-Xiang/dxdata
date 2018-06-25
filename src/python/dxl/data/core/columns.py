from collections import namedtuple
import abc
import uuid
from typing import NamedTuple, Dict, Tuple, Optional, List
import numpy as np

Size = Optional[int]


class Columns:
    """
    A abstract representation of **streamed** multi-column data.
    """
    pass

    def __init__(self, dataclass: NamedTuple):
        self.dataclass = dataclass

    @property
    def columns(self):
        return self.dataclass._fields

    @property
    def capacity(self) -> Size:
        raise NotImplementedError

    @property
    def shapes(self) -> Dict[str, List[Size]]:
        return {
            k: [self.capacity] + v
            for k, v in self.dataclass.shapes().items()
        }

    @property
    def dtypes(self) -> Dict[str, type]:
        return self.dataclass.dtypes()

    def __iter__(self):
        raise NotImplementedError


class ColumnsWithIndex(Columns):
    def __getitem__(self, index) -> NamedTuple:
        raise NotImplementedError

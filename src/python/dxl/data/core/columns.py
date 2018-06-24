from collections import namedtuple
import abc
import uuid
from typing import NamedTuple, Dict, Tuple, TypeVar, List
import numpy as np

Size = TypeVar('Size', int, None)


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

    def capacity(self) -> Size:
        raise NotImplementedError

    def shapes(self) -> Dict[str, List[Size]]:
        return {
            k: [self.capacity] + v
            for k, v in self.dataclass.shapes.items()
        }

    def dtypes(self) -> Tuple[type]:
        return self.dataclass.dtypes

    def __iter__(self):
        raise NotImplementedError


class IndexedColumns(Columns):
    def __getitem__(self, index) -> NamedTuple:
        raise NotImplementedError
from enum import Enum
from functools import reduce
from typing import Iterable, Tuple

import numpy as np
import pandas as pd
from dxl.fs import Path


class Data:
    """
    Baseclass of data. Which is designed to be immutable, and processed by calling its methods to produce new data.
    """

    def __init__(self, data):
        self._data = data

    @classmethod
    def from_(cls, data):
        return cls(data)

    def to(self, constructor):
        return constructor(self.data())

    def data(self):
        return self._data

    @property
    def d(self):
        """
        Alias to self.data
        """
        return self._data


class DataIterable(Data):
    """
    Base class for iterable(list, tuple) of data.
    """

    def __init__(self, data: Iterable[Data]):
        super().__init__(data)

    def map(self, func) -> 'DataIterable':
        return DataIterable(list(map(func, self.d)))

    def filter(self, func) -> 'DataIterable':
        return DataIterable(list(filter(func, self.d)))

    def map_call(self, func_name, *args, **kwargs) -> 'DataIterable':
        """
        Call member method with func_name for each entry of data.
        """
        return self.map(lambda x: getattr(x, func_name)(*args, **kwargs))

    def map_to(self, constructor) -> 'DataIterable':
        return self.map(lambda x: constructor(x))

    def zip(self, data: 'DataIterable'):
        return DataIterable(zip(self.d, data.d))

    def first(self) -> Data:
        if isinstance(self.d, (list, tuple)):
            return self.d[0]
        else:
            return next(self.d)

    def flatten(self) -> 'DataIterable':
        result = []
        for d in self.data():
            if not isinstance(d, DataIterable):
                raise TypeError(
                    "Flatten requires Results of Results, got {}.".format(type(d)))
            result += d.to_list()
        return DataIterable(result)

    def merge(self, initializer=None) -> Data:
        """
        Call merge method on data, like reduce. 
        """
        result = initializer
        for o in self.data():
            if result is None:
                result = o
            else:
                result = result.merge(o)
        return result

    def to_list(self):
        return list(self.d)

    def __iter__(self):
        for d in self.data():
            yield d


class DataIterableWithKeys(DataIterable):
    def __init__(self, data: Iterable[Tuple]):
        if isinstance(data, DataIterable):
            super().__init__(data.data())
        elif isinstance(data, dict):
            super().__init__(data.items())
        else:
            super().__init__(data)

    def drop_keys(self) -> DataIterable:
        return self.map(lambda x: x[1])

    def to_dict(self):
        return {d[o]: d[1] for d in self.data()}

    def select(self, key) -> Data:
        for d in self.data():
            if d[0] == key:
                return d[1]
        raise KeyError("Key {} not found.".format(key))

    def select_all(self, key) -> DataIterable:
        result = []
        for d in self.data():
            if d[0] == key:
                result.append(d[1])
        return result


class DataNDArray(Data):
    @classmethod
    def convert_data_to_ndarray(cls, data):
        import numpy as np
        if isinstance(data, DataIterable):
            data = [d.data() for d in data.data()]
        if isinstance(data, Data):
            data = data.data()
        if isinstance(data, (list, tuple)):
            data = [d.data() if isinstance(d, Data) else d for d in data]
        return np.array(data)

    def __init__(self, data):
        super().__init__(self.convert_data_to_ndarray(data))

    @classmethod
    def from_(cls, data) -> 'DataNDArray':
        if isinstance(data, DataIterable):
            result = []
            for d in data:
                result.append(np.array(d.data()))
            return cls(np.array(result))


# class ParticleID(Enum):
#     Gamma = 22


# class ColumnNames:
#     Event = 'eventID'
#     Process = 'processName'
#     Particle = 'particalID'
#     SourceX = 'srcX'
#     SourceY = 'srcY'
#     SourceZ = 'srcZ'
#     X = 'x'
#     Y = 'y'
#     Z = 'z'
#     EnergyDeposit = 'energy'


# class ResultsDask(ResultBase):
#     def map(self, func) -> 'ResultsDask':
#         return Results(dask.delayed(map)(func, self.d))


# class ResultsNamedTuple(ResultBase):
#     pass


# class ResultsWithKeys(Results):
#     def __init__(self, data: Tuple[Tuple[str, ResultBase]]):
#         super().__init__(data)

#     def drop_keys(self) -> Results:
#         return self.map(lambda x: x[1])

#     def to_dict(self):
#         return {o[0]: o[1] for o in self.d}

#     def select(self, key):
#         for o in self.d:
#             if o[0] == key:
#                 return o[1]
#         raise KeyError("Key {} not found.".format(key))


# class ResultsWithUnknownKeys(ResultsDask):
#     def select(self, key):
#         return DataFrame(self.d.get_group(key))

#     def drop_keys(self) -> ResultsDask:
#         return self.map(lambda x: x[1])


# class Series(ResultBase):
#     def __init__(self, series: pd.Series):
#         super().__init__(series)

#     def columns(self, *cols):
#         return (self.d[c] for c in cols)

#     def position(self) -> 'Vec3':
#         return Vec3(*self.columns(ColumnNames.X,
#                                   ColumnNames.Y,
#                                   ColumnNames.Z))

#     def source_position(self) -> 'Vec3':
#         return Vec3(*self.columns(ColumnNames.SourceX,
#                                   ColumnNames.SourceY,
#                                   ColumnNames.SourceZ))

#     def energy_deposit(self) -> float:
#         return self.d[ColumnNames.EnergyDeposit]


# class DataFrame(ResultBase):
#     def __init__(self, dataframe: pd.DataFrame):
#         super().__init__(dataframe)

#     def first(self, *columns) -> Series:
#         return Series(self.d.iloc[0])

#     def split_by(self, column: str) -> ResultsWithKeys:
#         groups = self.d.groupby(column)
#         if isinstance(groups, DataFrameGroupBy):
#             return ResultsWithUnknownKeys(groups)
#         else:
#             return ResultsWithKeys(((k, DataFrame(groups.get_group(k).drop([column], axis=1))) for k in groups.groups))

#     def split_row(self) -> Results:
#         return Results((Series(self.d.iloc[i]) for i in range(self.d.shape[0])))

#     def merge(self, r) -> 'DataFrame':
#         if not isinstance(r, DataFrame):
#             raise TypeError(
#                 "Can not merge {} with {}.".format(__class__, type(r)))
#         return DataFrame(pd.concat([self.d, r.d], axis=0))

#     def to_event(self) -> 'Event':
#         if not ColumnNames.Event in self.d.columns:
#             return Event(self.d)


# class Vec3(ResultBase):
#     def __init__(self, x, y=None, z=None):
#         super().__init__(np.array([x, y, z]))

#     @property
#     def x(self) -> float:
#         return self.d[0]

#     @property
#     def y(self) -> float:
#         return self.d[1]

#     @property
#     def z(self) -> float:
#         return self.d[2]

#     def to_list(self):
#         return tuple(self.d)


# class EnergyDeposit(ResultBase):
#     def __init__(self, position, energy):
#         super().__init__((position, energy))

#     @property
#     def position(self):
#         return self.d[0]

#     @property
#     def energy(self):
#         return self.d[1]


# class Event(DataFrame):
#     def __init__(self, dataframe: pd.DataFrame):
#         super().__init__(dataframe)

#     def source_position(self) -> Vec3:
#         return self.first().source_position()

#     def first_position(self) -> Vec3:
#         return self.first().position()

#     def incident_direction(self) -> Vec3:
#         dp = self.first_position().d - self.source_position().d
#         return Vec3(*tuple(dp / np.linalg.norm(dp)))

#     def energy_deposit_list(self) -> Results:
#         return self.split_row().map(lambda s: EnergyDeposit(s.position(), s.energy_deposit()))

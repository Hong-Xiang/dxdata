from .core import Data, DataIterable, DataIterableWithKeys
from .geometry import VectorLowDim
import pandas as pd


class Series(Data):
  def __init__(self, series: pd.Series):
    super().__init__(series)

  def columns(self, *cols):
    return DataIterable([self.d[c] for c in cols])


class DataFrame(Data):
  def __init__(self, data):
    if not isinstance(data, pd.DataFrame):
      data = pd.DataFrame(data=data)
    super().__init__(data)

  def nb_rows(self):
    return self.data().shape[0]

  def first(self) -> Series:
    return Series(self.d.iloc[0])

  def split_by(self, column: str) -> DataIterableWithKeys:
    groups = self.d.groupby(column)
    return DataIterableWithKeys([(k,
                                  DataFrame((groups.get_group(k).drop(
                                      [column], axis=1))))
                                 for k in groups.groups])

  def split_row(self) -> DataIterable:
    return DataIterable(
        [Series(self.d.iloc[i]) for i in range(self.nb_rows())])

  def merge(self, r) -> 'DataFrame':
    if not isinstance(r, DataFrame):
      raise TypeError("Can not merge {} with {}.".format(__class__, type(r)))
    return DataFrame(pd.concat([self.d, r.d], axis=0))

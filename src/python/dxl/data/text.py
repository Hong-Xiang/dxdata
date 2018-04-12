from dxl.fs import Path
from .core import Data
import pandas as pd


class DataCSV(Data):
  def __init__(self, path: str):
    super().__init__(Path(path))

  def load(self, cls=None) -> 'dxl.data.DataFrame':
    from .pandas_ import DataFrame
    if cls is None:
      cls = DataFrame
    if cls == DataFrame:
      return DataFrame(pd.read_csv(self.d.s))

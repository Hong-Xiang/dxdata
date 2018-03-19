from .core import Data
import pandas as pd


class DataFrame(Data):
    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data=data)
        super().__init__(data)

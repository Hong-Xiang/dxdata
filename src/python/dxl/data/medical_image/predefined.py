from .gate import ParticleID, ColumnNames, RootData
from ..text import DataCSV
from ..core import DataNDArray
from dxl.fs import File
import pandas as pd
import numpy as np


def gamma_incident_directions(csv_filename) -> pd.DataFrame:
    events = (DataCSV('hits.csv').load()
              .to(RootData)
              .split_by_event())
    inci_dirs = (events
                 .map_call('incident_direction')
                 .map(lambda d: d.d)
                 .to(DataNDArray))
    return pd.DataFrame(data=np.array(inci_dirs.d), columns=['x', 'y', 'z'])


def gamma_energy_deposit_samples(csv_filename):
    events = (DataCSV('hits.csv').load()
              .to(RootData)
              .split_by_event())
    eps = events.map_call('energy_deposit_list').flatten()
    poss = eps.map_call('position')
    engs = eps.map_call('energy')
    result = (poss.zip(engs)
              .map(lambda t: tuple(list(t[0].data()) + [t[1]]))
              .to(DataNDArray))
    return pd.DataFrame(data=np.array(result.d),
                        columns=['x', 'y', 'z', 'energy'])

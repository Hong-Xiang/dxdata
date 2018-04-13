from ..core import Data, DataIterable
from ..pandas_ import Series, DataFrame
from ..geometry import Vector3
from enum import Enum
import pandas as pd
import numpy as np


class ParticleID(Enum):
    Gamma = 22


class ColumnNames:
    Event = 'eventID'
    Process = 'processName'
    Particle = 'particalID'
    SourceX = 'srcX'
    SourceY = 'srcY'
    SourceZ = 'srcZ'
    X = 'x'
    Y = 'y'
    Z = 'z'
    EnergyDeposit = 'energy'


class RootStep(Series):
    def position(self) -> Vector3:
        return Vector3(self.columns(ColumnNames.X,
                                    ColumnNames.Y,
                                    ColumnNames.Z))

    def source_position(self) -> Vector3:
        return Vector3(self.columns(ColumnNames.SourceX,
                                    ColumnNames.SourceY,
                                    ColumnNames.SourceZ))

    def energy_deposit(self) -> Data:
        return self.columns(ColumnNames.EnergyDeposit).first()


class RootData(DataFrame):
    def split_by_event(self) -> DataIterable:
        return (self.split_by(ColumnNames.Event)
                .drop_keys()
                .map(lambda d: d.to(Event)))

    def to_event(self) -> 'Event':
        if not ColumnNames.Event in self.d.columns:
            return Event(self.d)

    def first(self):
        return super().first().to(RootStep)


class EnergyDeposit(Data):
    def __init__(self, position, energy):
        super().__init__((position, energy))

    def position(self):
        return self.d[0]

    def energy(self):
        return self.d[1]


class Event(DataFrame):
    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe)

    def first_step(self):
        return self.first().to(RootStep)

    def split_by_step(self) -> DataIterable:
        return self.split_row().map(lambda d: d.to(RootStep))

    def source_position(self) -> Vector3:
        return self.first_step().source_position()

    def first_position(self) -> Vector3:
        return self.first_step().position()

    def incident_direction(self) -> Vector3:
        dp = self.first_position().d - self.source_position().d
        return Vector3(tuple(dp / np.linalg.norm(dp)))

    def energy_deposit_list(self) -> DataIterable:
        return self.split_by_step().map(lambda s: EnergyDeposit(s.position(),
                                                             s.energy_deposit()))

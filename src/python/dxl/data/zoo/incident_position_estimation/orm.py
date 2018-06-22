"""
ORM definition
"""
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

import hashlib

from dxl.data.database import Base


class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(Integer, primary_key=True)
    hash = Column(String(40))


class Coincidence(Base):
    __tablename__ = 'coincidences'
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship(Experiment)
    type = Column(SmallInteger)
    events = relationship('Event', order_by='Event.index')

    def __repr__(self):
        return "<Coincidence(id={}, type={}, events={})>".format(
            self.id, self.type, self.events)


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship(Experiment)
    coincidence_id = Column(Integer, ForeignKey('coincidences.id'))
    photons = relationship('Photon', order_by='Photon.index')

    def __repr__(self):
        return "<Event(id={}, index={}, expr={}, photons={})>".format(
            self.id, self.index, self.experiment.hash[:4], self.photons)


class Photon(Base):
    __tablename__ = 'photons'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship("Experiment")
    event_id = Column(Integer, ForeignKey('events.id'))
    hits = relationship('Hit', order_by='Hit.index')

    def __repr__(self):
        return "<Photon(id={}, index={}, hits={})>".format(
            self.id, self.index, self.hits)


class Crystal(Base):
    __tablename__ = 'crystals'
    id = Column(Integer, primary_key=True)
    crystal_id = Column(Integer)
    block_id = Column(Integer)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship(Experiment)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    width = Column(Float)
    height = Column(Float)
    depth = Column(Float)
    normal_x = Column(Float)
    normal_y = Column(Float)
    normal_z = Column(Float)

    def __repr__(self):
        return "<Crystal(center=({}, {}, {}), shape=({}, {}, {}), normal=({}, {}, {}))>".format(
            self.x, self.y, self.z, self.width, self.height, self.depth,
            self.normal_x, self.normal_y, self.normal_z)


class Hit(Base):
    __tablename__ = 'hits'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship(Experiment)
    photon_id = Column(Integer, ForeignKey('photons.id'))
    crystal_id = Column(Integer, ForeignKey('crystals.id'))
    crystal = relationship(Crystal)

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    energy = Column(Float)
    time = Column(Float)

    def __repr__(self):
        return "<Hit(id={}, index={}, x={}, y={}, z={}, energy={}, time={})>".format(
            self.id, self.index, self.x, self.y, self.z, self.energy,
            self.time)

    def to_list(self, columns=None):
        if columns is None:
            columns = ('x', 'y', 'z', 'energy', 'index')
        return [getattr(self, c) for c in columns]

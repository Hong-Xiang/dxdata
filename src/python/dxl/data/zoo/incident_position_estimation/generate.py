"""
Convert csv data to database.
"""
import json
import time
from functools import wraps

import click
import numpy as np
import pandas
from tqdm import tqdm

from dxl.core.debug import enter_debug
from dxl.core.logger import Logger
from dxl.core.logger.utils import set_logging_info_level_with_default_format
from dxl.data.database import create_all, get_or_create_session

from .orm import Coincidence, Crystal, Event, Experiment, Hit, Photon
from .crystal import ScannerSpec, CrystalFactory, CrystalID2

import hashlib

enter_debug()

logger = Logger('incident_position_estimation')
set_logging_info_level_with_default_format()

NB_CHUNK = 1000


class auto_flush:
    def __init__(self, nb_chunk=None):
        if nb_chunk is None:
            nb_chunk = NB_CHUNK
        self.nb_chunk = nb_chunk
        self.nb_called = 0

    def __call__(self, func):
        @wraps(func)
        def caller(obj, session, *args, **kwargs):
            result = func(obj, session, *args, **kwargs)
            self.nb_called += 1
            if self.nb_called % self.nb_chunk == 0:
                session.flush()
            return result

        return caller


class DataSpec:
    def __init__(self, hits_csv, coincidence_csv, target_path):
        self.hits_csv = hits_csv
        self.coincidence_csv = coincidence_csv
        self.target_path = target_path


def load_data(s: DataSpec):
    coincidence = pandas.read_csv(s.coincidence_csv)
    hits = pandas.read_csv(s.hits_csv)
    return hits, coincidence


class Experiments:
    def __init__(self):
        self.experiment = None

    def make(self, session, files):
        e = Experiment(hash=self.get_experiment_hash(files))
        session.add(e)
        return e

    def make_and_store(self, session, files):
        self.experiment = self.make(session, files)
        return self.experiment

    def get(self):
        return self.experiment

    def get_experiment_hash(self, files):
        sha1 = hashlib.sha1()
        for p in files:
            with open(p, 'r') as fin:
                sha1.update(fin.read().encode())
        return sha1.hexdigest()


class Crystals:
    def __init__(self, spec=None):
        self.factory = CrystalFactory(spec)
        self.data = {}

    def set_spec(self, spec):
        self.factory = CrystalFactory(spec)

    def make(self, session, experiment, crystal_id, block_id):
        cid2 = CrystalID2(crystal_id, block_id)
        c_obj = self.factory.create(cid2)
        origin = c_obj.entity.origin()
        shape = c_obj.entity.shape()
        normal = c_obj.entity.normal()
        c_db = Crystal(
            crystal_id=cid2.crystal_id,
            block_id=cid2.block_id,
            experiment=experiment,
            x=origin.x(),
            y=origin.y(),
            z=origin.z(),
            width=shape.x(),
            height=shape.y(),
            depth=shape.z(),
            normal_x=normal.x(),
            normal_y=normal.y(),
            normal_z=normal.z())
        session.add(c_db)
        return c_db

    @auto_flush()
    def make_and_store(self, session, experiment, crystal_id, block_id):
        self.data[(crystal_id, block_id)] = self.make(session, experiment,
                                                      crystal_id, block_id)

    def process_all(self, session, scanner_spec, experiment):
        for ic in range(scanner_spec.nb_detectors_per_block):
            for ib in range(scanner_spec.nb_blocks):
                self.make_and_store(session, experiment, ic, ib)
        session.flush()

    def get(self, crystal_id, block_id):
        return self.data.get((crystal_id, block_id))


class Photons:
    def __init__(self):
        self.data = {}

    def get(self, eid, pid):
        return self.data.get((eid, pid))

    def make(self, session, eid, pid, experiment, events):
        p = Photon(index=pid, experiment=experiment, hits=[])
        events.get(eid).photons.append(p)
        session.add(p)
        return p

    def get_or_create(self, session, eid, pid, events, experiment):
        if self.get(eid, pid) is None:
            self.data[(eid, pid)] = self.make(session, eid, pid, experiment,
                                              events)
        return self.get(eid, pid)


class Events:
    def __init__(self):
        self.data = {}

    def get(self, eid):
        return self.data.get(eid)

    @auto_flush()
    def make(self, session, eid, photons, experiment):
        e = Event(index=int(eid), photons=[], experiment=experiment)
        session.add(e)
        return e

    def get_or_create(self, session, eid, photons, experiment):
        if self.get(eid) is None:
            self.data[eid] = self.make(session, eid, photons, experiment)
        return self.get(eid)


class Hits:
    def make(self, session, row, experiment, crystal):
        hit = Hit(
            x=row['posX'],
            y=row['posY'],
            z=row['posZ'],
            energy=row['edep'],
            time=row['time'],
            experiment=experiment,
            crystal=crystal)
        session.add(hit)
        return hit

    @auto_flush()
    def process_row(self, session, row, events, photons, crystals, experiment):
        cid, bid = int(row['crystalID']), int(row['blockID'])
        hit = self.make(session, row, experiment, crystals.get(cid, bid))
        eid, pid = int(row['eventID']), int(row['photonID'])
        e = events.get_or_create(session, eid, photons, experiment)
        p = photons.get_or_create(session, eid, pid, events, experiment)
        p.hits.append(hit)
        hit.index = len(p.hits) - 1
        return hit

    @logger.before.info('Processing rows...')
    @logger.after.info('Process row done.')
    def process_all(self, session, hits_data, experiment, events, photons,
                    crystals):
        for i in tqdm(range(hits_data.shape[0]), ascii=True):
            self.process_row(session, hits_data.iloc[i], events, photons,
                             crystals, experiment)
        session.flush()


class Coincidences:
    @auto_flush()
    def make(self, session, row, events, experiment):
        c = Coincidence(
            events=[
                events.get(int(row['eventID1'])),
                events.get(int(row['eventID2']))
            ],
            type=(int(row['type(0:scatter-1:random-2:true)'])),
            experiment=experiment)
        session.add(c)
        return c

    @logger.before.info('Processing conincidences...')
    @logger.after.info('Done.')
    def process_all(self, session, conincidence_data, experiment, events):
        for i in tqdm(range(conincidence_data.shape[0]), ascii=True):
            self.make(session, conincidence_data.iloc[i], events, experiment)
        session.flush()


class DataSpec:
    def __init__(self, scanner_json, hits_csv, coincidences_csv, target_path):
        self.scanner_json = scanner_json
        self.hits_csv = hits_csv
        self.coincidence_csv = coincidences_csv
        self.target_path = target_path

    def files(self):
        return [self.scanner_json, self.hits_csv, self.coincidence_csv]

    def __repr__(self):
        return "<DataSpec(scanner_json={},\n{ind}hits_csv={},\n{ind}coincidence_csv={},\n{ind}target_path={})>".format(
            self.scanner_json,
            self.hits_csv,
            self.coincidence_csv,
            self.target_path,
            ind=" " * 10)


class DatabaseGenerator:
    def __init__(self, data_spec: DataSpec):
        self.spec = data_spec
        self.experiments = Experiments()
        self.crystals = Crystals()
        self.hits = Hits()
        self.events = Events()
        self.photons = Photons()
        self.coincidences = Coincidences()

    @logger.before.info('Loading data...')
    @logger.after.info('Loading data done.')
    def load_data(self):
        with open(self.spec.scanner_json, 'r') as fin:
            scanner_spec = ScannerSpec(**json.load(fin))
        hits_data = pandas.read_csv(self.spec.hits_csv)
        coincidences_data = pandas.read_csv(self.spec.coincidence_csv)
        return scanner_spec, hits_data, coincidences_data

    @logger.before.info('Generating database ...')
    @logger.after.info('Generating database done.')
    def generate(self):
        self.session = session = self.make_session()
        experiment = self.experiments.make_and_store(session,
                                                     self.spec.files())
        scanner_spec, hits_data, coincidence_data = self.load_data()
        self.crystals.set_spec(scanner_spec)
        self.crystals.process_all(session, scanner_spec, experiment)
        self.hits.process_all(session, hits_data, experiment, self.events,
                              self.photons, self.crystals)
        self.coincidences.process_all(session, coincidence_data, experiment,
                                      self.events)
        self.commit()

    def make_session(self):
        create_all(self.spec.target_path)
        return get_or_create_session(self.spec.target_path)

    @logger.before.info('committing...')
    @logger.after.info('commit done.')
    def commit(self):
        self.session.commit()

    def flush(self):
        self.session.flush()


# def generate_database(scanner_json, coincidence_csv, hits_csv, target):
#     generator = DatabaseGenerator(scanner_json, coincidence_csv, hits_csv, target)
#     s = DataSpec(hits_csv, coincidence_csv, target)
#     hits_data, coincidences_data = load_data(s)
#     make_session(target)
#     make_experiment(s)
#     process_rows(hits_data)
#     flush()
#     make_coincidences(coincidences_data)
#     commit()
#     Processing.session.close()

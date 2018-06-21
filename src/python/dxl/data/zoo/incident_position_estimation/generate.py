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

enter_debug()

logger = Logger('incident_estimation')
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
        def caller(session, *args, **kwargs):
            result = func(session, *args, **kwargs)
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


class Crystals:
    def __init__(self, spec):
        self.factory = CrystalFactory(spec)
        self.data = {}

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

    def make_and_store(self, session, experiment, crystal_id, block_id):
        self.data[(crystal_id, block_id)] = self.make(session, experiment,
                                                      crystal_id, block_id)

    def get(self, crystal_id, block_id):
        return self.data.get((crystal_id, block_id))


class Experiments:
    def __init__(self, generator):
        self.g = generator
        self.experiments = None

    def make(self, files, session):
        e = Experiment(hash=get_experiment_hash(files))
        session.add(e)
        return e

    def get_experiment_hash(files):
        sha1 = hashlib.sha1()
        for p in files:
            with open(p, 'r') as fin:
                sha1.update(fin.read().encode())
        return sha1.hexdigest()


class Photons:
    def __init__(self, generator):
        self.g = generator
        self.photons = {}

    def get(self, eid, pid):
        return self.photons.get(eid, {}).get(pid)

    def make(self, eid, pid):
        p = Photon(index=pid, experiment=Processing.experiment, hits=[])
        self.g.events.get(eid).photons.append(p)
        self.g.session.add(p)
        return p

    def get_or_create(eid, pid):
        if self.get(eid, pid) is None:
            self.photons[eid][pid] = self.make(eid, pid)
        return self.get(eid, pid)


class Events:
    def __init__(self, generator):
        self.g = generator
        self.events = {}

    def get(eid):
        return self.events.get(eid)

    def make(eid):
        e = Event(
            index=int(eid),
            photons=[],
            experiment=self.g.experiment.experiment)
        self.g.session.add(e)
        self.g.photons.photons[eid] = {}
        return e

    def get_or_create(eid):
        if self.get(eid) is None:
            self.events[eid] = self.make(eid)
        return self.get(eid)


class Hits:
    def __init__(self, generator):
        self.g = generator

    def make(self, session, row):
        hit = Hit(
            x=row['posX'],
            y=row['posY'],
            z=row['posZ'],
            energy=row['edep'],
            time=row['time'],
            experiment=Processing.experiment)
        session.add(hit)
        return hit

    def process_row(self, session, row, events, photons):
        hit = self.make(session, row)
        eid, pid = int(row['eventID']), int(row['photonID'])
        e = events.get_or_create(eid)
        p = photons.get_or_create(eid, pid)
        p.hits.append(hit)
        hit.index = len(p.hits) - 1
        return hit

    @logger.before.info('Processing rows...')
    @logger.after.info('Process row done.')
    def process_all_hits(self, session, hits_data):
        for i in tqdm(range(hits_data.shape[0]), ascii=True):
            self.process_row(session, hits_data.iloc[i])
            if i % NB_CHUNK == 0:
                flush()


@logger.before.info('committing...')
@logger.after.info('commit done.')
def commit():
    Processing.session.commit()


def flush():
    Processing.session.flush()


def make_coincidence(row):
    c = Coincidence(
        events=[
            get_event(int(row['eventID1'])),
            get_event(int(row['eventID2']))
        ],
        type=(int(row['type(0:scatter-1:random-2:true)'])),
        experiment=Processing.experiment)
    Processing.session.add(c)
    return c


def make_coincidences(conincidence_data):
    for i in tqdm(range(conincidence_data.shape[0]), ascii=True):
        make_coincidence(conincidence_data.iloc[i])
        if i % NB_CHUNK == 0:
            flush()


class DatabaseGenerator:
    def __init__(self, scanner_json, hits_csv, coincidence_csv, target_path):
        self.scanner_json = scanner_json
        self.hits_csv = hits_csv
        self.conincidence_csv = coincidence_csv
        self.target_path = target_path
        self.experiments = Experiments()
        self.crystals = Crystals()
        self.hits = Hits(self)
        self.hits = Hits(self)
        self.hits = Hits(self)
        self.hits = Hits(self)

    @logger.before.info('Loading data...')
    @logger.after.info('Loading data done.')
    def load_data(s: DataSpec):
        with open(self.scanner_json, 'r') as fin:
            scanner_spec = json.load(fin)
        hits_data = pandas.read_csv(s.hits_csv)
        coincidences_data = pandas.read_csv(s.coincidence_csv)
        return scanner_spec, hits_data, coincidences_data

    def generate(self):
        self.session = self.make_session()
        self.experiments.experiment = self.experiments.make(
            [self.scanner_json, self.hits_csv, self.conincidence_csv],
            self.session)
        scanner_spec, hits_data, coincidence_data = self.load_data()
        self.crystals.process(scanner_spec)
        self.hits.process(hits_data)
        self.coincidences.process(coincidence_data)

    def make_session(self):
        create_all(self.target_path)
        return get_or_create_session(self.target_path)


@logger.before.info(
    'Generating database from:\nCoincidence csv: {coincidence_csv},\nHits csv: {hits_csv},\nTarget: {target}.\n'
)
@logger.after.info('Done.')
def generate_database(scanner_json, coincidence_csv, hits_csv, target):
    s = DataSpec(hits_csv, coincidence_csv, target)
    hits_data, coincidences_data = load_data(s)
    make_session(target)
    make_experiment(s)
    process_rows(hits_data)
    flush()
    make_coincidences(coincidences_data)
    commit()
    Processing.session.close()

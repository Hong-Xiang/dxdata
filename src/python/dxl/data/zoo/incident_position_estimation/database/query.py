from contextlib import contextmanager
from pprint import pprint
from types import SimpleNamespace

import click
import numpy as np
from sqlalchemy.orm import joinedload, subqueryload, selectinload

from dxl.data.database.engine import session_factory, session_scope
from dxl.data.function import function
from tqdm import tqdm

from .orm import Coincidence, Crystal, Event, Experiment, Hit, Photon


@contextmanager
def query_scope(path):
    with session_scope(session_factory(path)) as sess:
        yield sess


__all__ = ['nb', 'chunked']


class nb(SimpleNamespace):
    @classmethod
    def hits(cls, path):
        with query_scope(path) as sess:
            return sess.query(Hit).count()

    @classmethod
    def photon(cls, path):
        with query_scope(path) as sess:
            return sess.query(Photon).count()

    @classmethod
    def crystal(cls, path):
        with query_scope(path) as sess:
            return sess.query(Crystal).count()

    @classmethod
    def experiments(cls, path):
        with query_scope(path) as sess:
            return sess.query(Experiment).distinct().count()


class chunked(SimpleNamespace):
    @classmethod
    def chunked_query(cls, q, func, limit, offset):
        if offset is not None:
            q = q.offset(offset)
        if limit is not None:
            q = q.limit(limit)
        return func(q.all())

    @classmethod
    def photon_hits(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            q = sess.query(Photon).options(subqueryload(Photon.hits))
            return cls.chunked_query(q, func, limit, offset)

    @classmethod
    def photon_hits2(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            q = (sess.query(Photon)
                 .options(subqueryload(Photon.hits)
                          .subqueryload(Hit.crystal)))
            return cls.chunked_query(q, func, limit, offset)

    @classmethod
    def photon_hits3(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            q = sess.query(Photon).options(selectinload(Photon.hits))
            return cls.chunked_query(q, func, limit, offset)

    @classmethod
    def photon_hits4(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            q = (sess.query(Photon)
                 .options(selectinload(Photon.hits)
                          .selectinload(Hit.crystal)))
            return cls.chunked_query(q, func, limit, offset)

    @classmethod
    def photon_hits5(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            q = sess.query(Photon).options(
                joinedload(Photon.hits, innerjoin=True))
            return cls.chunked_query(q, func, limit, offset)

    @classmethod
    def photon_hits6(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            q = (sess.query(Photon)
                 .options(joinedload(Photon.hits, innerjoin=True)
                          .joinedload(Hit.crystal, innerjoin=True)))
            return cls.chunked_query(q, func, limit, offset)

    @classmethod
    def photon(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            q = sess.query(Photon)
            return cls.chunked_query(q, func, limit, offset)

    @classmethod
    def coincidence(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            return cls.chunked_query(sess.query(Coincidence), func, limit, offset)

    # @classmethod
    # def coincidence_events(cls, path, func, limit=None, offset=None):
    #     with query_scope(path) as sess:
    #         return cls.chunked_query(sess.query(Coincidence.events)
    #                                  .options(joinedload(Event.photons)), func, limit, offset)

    @classmethod
    def coincidence_events(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            return cls.chunked_query(sess.query(Coincidence.events), func, limit, offset)

    # @classmethod
    # def photon_hits_crystal(cls, path, func, limit=None, offset=None):
    #     with query_scope(path) as sess:
    #         q = (sess.query(Photon)
    #              .options(joinedload(Photon.hits, innerjoin=True)
    #                       .joinedload(Hit.crystal, innerjoin=True)))
    #         return cls.chunked_query(q, func, limit, offset)

    # @classmethod
    # def coincidence_photon_hits_crystal(cls, path, func, limit=None, offset=None):
    #     with query_scope(path) as sess:
    #         q = (sess.quary(Coincidence)
    #              .option(joinedload(Coincidence.events, innerjoin=True)
    #                      .joinedload(Event.photons, innerjoin=True)
    #                      .joinedload(Photon.hits, innerjoin=True)
    #                      .joinedload(Hit.crystal, innerjoin=True)))
    #         return cls.chunked_query(q, func, limit, offset)

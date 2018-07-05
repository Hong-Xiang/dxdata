from contextlib import contextmanager
from pprint import pprint
from types import SimpleNamespace

import click
import numpy as np
from sqlalchemy.orm import joinedload, selectinload, subqueryload

from dxl.data.database.engine import session_factory, session_scope

from .orm import Coincidence, Crystal, Event, Experiment, Hit, Photon


@contextmanager
def query_scope(path):
    with session_scope(session_factory(path)) as sess:
        yield sess


__all__ = ['nb', 'single', 'chunked']


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
    
    @classmethod
    def coincidence(cls, path):
        with query_scope(path) as sess:
            return sess.query(Coincidence).count()

class single(SimpleNamespace):
    @classmethod
    def hit(cls, path, func, offset=0):
        with query_scope(path) as sess:
            return func(sess.query(Hit).offset(offset).first())
    
    @classmethod
    def photon(cls, path, func, offset=0):
        with query_scope(path) as sess:
            return func(sess.query(Photon).offset(offset).first())
    
    @classmethod
    def coincidence(cls, path, func, offset=0):
        with query_scope(path) as sess:
            return func(sess.query(Coincidence).offset(offset).first())
            

class chunked(SimpleNamespace):
    @classmethod
    def chunked_query(cls, q, func, limit=None, offset=None):
        if offset is not None:
            q = q.offset(offset)
        if limit is not None:
            q = q.limit(limit)
        return func(q.all())

    @classmethod
    def photon(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            q = sess.query(Photon).options(subqueryload(Photon.hits))
            return cls.chunked_query(q, func, limit, offset)

    @classmethod
    def coincidence(cls, path, func, limit=None, offset=None):
        with query_scope(path) as sess:
            return cls.chunked_query(sess.query(Coincidence)
                                     .options(subqueryload(Coincidence.events)
                                              .subqueryload(Event.photons)
                                              .subqueryload(Photon.hits)), func, limit, offset)

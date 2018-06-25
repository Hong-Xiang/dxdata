from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

__all__ = [
    'Engine', 'Session', 'get_or_create_engine', 'get_or_create_session'
]

import os
import warnings

from sqlalchemy import event
from sqlalchemy import exc


def add_engine_pidguard(engine):
    """Add multiprocessing guards.

    Forces a connection to be reconnected if it is detected
    as having been shared to a sub-process.

    """

    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        connection_record.info['pid'] = os.getpid()

    @event.listens_for(engine, "checkout")
    def checkout(dbapi_connection, connection_record, connection_proxy):
        pid = os.getpid()
        if connection_record.info['pid'] != pid:
            # substitute log.debug() or similar here as desired
            warnings.warn(
                "Parent process %(orig)s forked (%(newproc)s) with an open "
                "database connection, "
                "which is being discarded and recreated." %
                {"newproc": pid, "orig": connection_record.info['pid']})
            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError(
                "Connection record belongs to pid %s, "
                "attempting to check out in pid %s" %
                (connection_record.info['pid'], pid)
            )


class Engine:
    instances = {}

    @classmethod
    def reset(cls):
        cls.instance = None

    @classmethod
    def get_or_create_engine(cls, path=None):
        path = str(path)
        if cls.instances.get(path) is None:
            cls.instances[path] = cls.create_engine(path)
            # add_engine_pidguard(cls.instance)
        return cls.instances[path]

    @classmethod
    def create_engine(cls, path):
        return create_engine('sqlite:///{}'.format(path), echo=False)


class Session:
    instances = {}
    maker = None

    @classmethod
    def reset(cls):
        cls.instance = None
        cls.maker = None

    @classmethod
    def get_or_create_session(cls, path=None):
        path = str(path)
        if cls.instances.get(path) is None:
            cls.instances[path] = scoped_session(sessionmaker(
                bind=Engine.get_or_create_engine(path)))
        return cls.instances[path]()


def get_or_create_engine(path=None):
    return Engine.get_or_create_engine(path)


def get_or_create_session(path=None):
    return Session.get_or_create_session(path)


def session_factory(path):
    connect = 'sqlite:///{}'.format(str(path))
    return scoped_session(sessionmaker(bind=create_engine(connect, isolation_level='READ_UNCOMMITTED')))


@contextmanager
def session_scope(session_factory):
    """Provide a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

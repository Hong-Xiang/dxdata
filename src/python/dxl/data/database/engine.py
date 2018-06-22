from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

__all__ = [
    'Engine', 'Session', 'get_or_create_engine', 'get_or_create_session'
]


class Engine:
    instance = None

    @classmethod
    def reset(cls):
        cls.instance = None

    @classmethod
    def get_or_create_engine(cls, path=None):
        if cls.instance is None:
            cls.instance = create_engine(
                'sqlite:///{}'.format(path), echo=False)
        return cls.instance


class Session:
    instance = None
    maker = None

    @classmethod
    def reset(cls):
        cls.instance = None
        cls.maker = None

    @classmethod
    def get_or_create_session(cls, path=None):
        if cls.instance is None:
            cls.maker = sessionmaker(bind=Engine.get_or_create_engine(path))
            cls.instance = Session.maker()
        return cls.instance


def get_or_create_engine(path=None):
    return Engine.get_or_create_engine(path)


def get_or_create_session(path=None):
    return Session.get_or_create_session(path)

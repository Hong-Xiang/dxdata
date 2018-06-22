from sqlalchemy.ext.declarative import declarative_base
from ..engine import get_or_create_engine

Base = declarative_base()


class Table:

    _created = False

    @classmethod
    def create_all(cls, path):
        if not cls._created:
            Base.metadata.create_all(get_or_create_engine(path))
            cls._created = True


def create_all(path):
    return Table.create_all(path)


__all__ = ['create_all']
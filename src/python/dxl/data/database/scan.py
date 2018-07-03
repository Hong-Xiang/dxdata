from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .engine import session_scope, session_factory
from collections import deque


# TODO: refactor, fetch common operations

class Chunked:
    pass


class DBScannerWith:
    def __init__(self, path, func):
        self.Session = session_factory(path)
        self.f = func

    def __iter__(self):
        def it():
            offset = 0
            while(True):
                with session_scope(self.Session) as sess:
                    result, offset = self.f(sess, offset)
                    if result is None:
                        break
                yield result
        return it()


class ChunkedDBScannerWith(DBScannerWith):
    def __init__(self, path, func, nb_buffer=4096):
        super().__init__(path, func)
        self.nb_buffer = nb_buffer

    def __iter__(self):
        def it():
            offset = 0
            is_end = False
            while(not is_end):
                with session_scope(self.Session) as sess:
                    result = self.f(sess, offset, self.nb_buffer)
                    offset += len(result)
                    if result is None or len(result) == 0:
                        is_end = True
                        result = []
                for r in result:
                    yield r
        return it()


class DBScannerFixedSession:
    def __init__(self, path, func):
        self.session = session_factory(path)()
        self.f = func

    def __iter__(self):
        def it():
            for x in self.f(self.session):
                yield x
        return it()

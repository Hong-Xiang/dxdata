from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .engine import session_scope, session_factory


class DBScannerWith:
    def __init__(self, path, func, nb_per_row=100):
        self.Session = session_factory(path)
        self.f = func
        self.nb_per_row = 64

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

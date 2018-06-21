from dxl.data.zoo.incident_position_estimation.generate import auto_flush, NB_CHUNK

import pytest


@pytest.fixture
def session_spy():
    class SessionSpy:
        def __init__(self):
            self.flushed = 0

        def flush(self):
            self.flushed += 1

    return SessionSpy()


def test_auto_flush(session_spy):
    @auto_flush()
    def foo(session):
        pass

    assert session_spy.flushed == 0
    for i in range(NB_CHUNK):
        foo(session_spy)
    assert session_spy.flushed == 1
    for i in range(NB_CHUNK):
        foo(session_spy)
    assert session_spy.flushed == 2

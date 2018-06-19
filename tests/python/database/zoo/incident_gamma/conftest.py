import pytest


@pytest.fixture(scope='module')
def path_of_db():
    return '/mnt/gluster/CustomerTests/IncidentEstimation/SQLAlchemyDemo/simu0.1/gamma.db'
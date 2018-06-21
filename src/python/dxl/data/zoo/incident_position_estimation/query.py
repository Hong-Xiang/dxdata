from dxl.data.database.engine import get_or_create_session
from .orm import Coincidence, Event, Photon, Hit
from tqdm import tqdm
import numpy as np
import click
from pprint import pprint

from contextlib import contextmanager


def bind_path(path):
    return get_or_create_session(path)


def nb_hits():
    return get_or_create_session().query(Hit).count()


def nb_photon():
    return get_or_create_session().query(Photon).count()


def phton_hits_with_first_hit(limit=None):
    q = (get_or_create_session().query(Photon, Hit)
         .filter(Hit.photon_id == Photon.id).filter(Hit.index == 0))
    if limit is not None:
        q = q.limit(limit)
    return q


def all_photon():
    return get_or_create_session().query(Photon)


def all_hits_group_by_photon(limit=10):
    return get_or_create_session().query(Photon.hits).limit(limit).all()


@contextmanager
def hits_generator():
    get_or_create_session().query(Photon.hits)


def get_first_hits_for_all_photon():
    columns = ['x', 'y', 'z', 'energy']
    for p, h in (query_phton_and_first_hit().limit(10)):
        print(p.hits)
        print(np.array([h.to_list(columns) for h in p.hits]))
        # print(p_hits)
        print(h.to_list(columns))


def all_first_hits_of_coincidences(coincidence_type=None):
    result = get_or_create_session().query(Coincidence,
                                           Hit).join(Event).join(Photon)
    if coincidence_type is not None:
        result = result.filter(Coincidence.type == coincidence_type)
    result = result.join(Hit).filter(Hit.index == 0)
    return result


def test():
    limit = 10
    # for p, h in tqdm(phton_and_first_hit(limit)):
    # print([h.to_list() for h in p.hits])
    # print(h.to_list())
    result = all_first_hits_of_coincidences().limit(limit).all()
    pprint(result)


@click.command()
@click.option(
    '--path',
    '-p',
    help='Database path',
    type=click.types.Path(True, dir_okay=False))
def cli(path):
    bind_path(path)
    test()


if __name__ == "__main__":
    cli()
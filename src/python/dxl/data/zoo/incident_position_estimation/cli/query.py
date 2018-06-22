import click

from dxl.data.database import create_all
from pprint import pprint


@click.group()
@click.option('--path', '-p', help='Path of database.')
@click.pass_context
def query(ctx, path):
    ctx.obj = {'PATH': path}


@query.command()
@click.argument('cls')
@click.pass_context
def nb(ctx, cls):
    from ..query import nb_photon, nb_hits, nb_crystal, nb_experiments
    func_map = {
        'hit': nb_hits,
        'hits': nb_hits,
        'photon': nb_photon,
        'crystal': nb_crystal,
        'crystals': nb_crystal,
        'experiment': nb_experiments,
        'experiments': nb_experiments
    }
    path = ctx.obj['PATH']
    create_all(path)
    print('Number of {} in {}:'.format(cls, path), func_map[cls.lower()]())


@query.command()
@click.argument('limit', type=int)
@click.option('--task', '-t')
@click.pass_context
def hits(ctx, limit, task):
    create_all(ctx.obj['PATH'])
    from ..query import hits_of_photon, hits_of_photon_with_crystal_center
    if task == 'crystal':
        source = hits_of_photon_with_crystal_center
    else:
        source = hits_of_photon
    for _, d in zip(range(limit), source()):
        pprint(d)


class Verifications:
    @classmethod
    def in_box(cls, d):
        from dxl.shape import Point, Box
        hit, c = d
        p = Point([hit.x, hit.y, hit.z])
        b = Box([c.width, c.height, c.depth], [c.x, c.y, c.z],
                [c.normal_x, c.normal_y, c.normal_z])
        return p.is_in(b)


@query.command()
@click.argument('limit', type=int)
@click.option('--task', '-t')
@click.pass_context
def verify(ctx, limit, task):
    create_all(ctx.obj['PATH'])
    from ..query import hit_crystal_tuple
    if task == 'in_box':
        source = hit_crystal_tuple
        tester = Verifications.in_box
    if task is None:
        return
    source = hit_crystal_tuple
    for _, d in zip(range(limit), source()):
        pprint(tester(d))


if __name__ == "__main__":
    query()
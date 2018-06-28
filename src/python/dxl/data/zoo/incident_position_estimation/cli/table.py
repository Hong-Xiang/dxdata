import click
import json


@click.command()
@click.option(
    '--path_db',
    '-d',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
@click.option(
    '--path_table',
    '-t',
    type=click.types.Path(exists=False, file_okay=True, dir_okay=False))
@click.option(
    '--config',
    '-c',
    type=click.types.Path(exists=True, file_okay=True, dir_okay=False))
def make(path_db, path_table, config):
    from ..table import make_table
    from ..dataclass import Hit, HitWithCrystalCenter, sort_hits_by_energy
    with open(config, 'r') as fin:
        c = json.load(fin)
    if c.get('is_exact_xyz'):
        hit_class = Hit
    else:
        hit_class = HitWithCrystalCenter
    padding_size = c.get('padding_size', 10)
    if c.get('shuffle', 'energy') == 'energy':
        shuffle = sort_hits_by_energy
    make_table(path_db, path_table, hit_class, padding_size, shuffle)

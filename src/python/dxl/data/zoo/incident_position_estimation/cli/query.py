import click


@click.group()
def query():
    pass


@query.command()
@click.option('--path', '-p', help='Path of database.')
@click.argument('cls')
def nb(path, cls):
    from ..query import nb_photon, nb_hits
    from dxl.data.database import create_all
    if cls.lower() in ('hit', 'hits'):
        create_all(path)
        print('Number of hits in {}:'.format(path), nb_hits())


if __name__ == "__main__":
    query()
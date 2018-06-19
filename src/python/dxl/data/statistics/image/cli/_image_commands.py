import click


@click.group()
def image():
    pass


@image.group()
def analysis():
    pass


@analysis.command()
@click.argument('target-path-file', type=click.Path(exists=True))
@click.argument('target-path-dataset', type=click.Path())
@click.option('--metric', '-m', type=str, multiple=True)
@click.option('--output', '-o', type=click.Path())
def single(target_path_file, target_path_dataset, metric, output):
    from ..statistics import analysis
    result = analysis({
        'type': 'h5',
        'path_file': target_path_file,
        'path_dataset': target_path_dataset
    }, None, metric, None, output)
    click.echo(str(result))

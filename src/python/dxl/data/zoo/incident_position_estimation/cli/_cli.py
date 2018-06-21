import click


class CLI(click.MultiCommand):
    commands = {
        'generate': None,
        'query': None,
    }

    def __init__(self):
        super(__class__, self).__init__(
            name='incident', help='Incident gamma estimation utilities.')

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from .query import query
        from .gen import generate
        if name in self.commands:
            if self.commands[name] is None:
                mapping = {'query': query, 'generate': generate}
                self.commands[name] = mapping.get(name)
        return self.commands.get(name)


incident = CLI()
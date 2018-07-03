import click


class CLI(click.MultiCommand):
    commands = {
        'make': None,
        'query': None,
        'table': None
    }

    def __init__(self):
        super().__init__(
            name='incident', help='Incident gamma estimation utilities.')

    def list_commands(self, ctx):
        return sorted(self.commands.keys())

    def get_command(self, ctx, name):
        from .query import query
        from .make import make
        if name in self.commands:
            if self.commands[name] is None:
                mapping = {'query': query, 'make': make}
                self.commands[name] = mapping.get(name)
        return self.commands.get(name)


incident = CLI()

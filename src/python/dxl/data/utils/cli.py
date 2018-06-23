import click


def build_cli_class(name, commands, locator, help_doc=None):
    class CLI(click.MultiCommand):
        commands = {c: None for c in commands}
        help_doc = help_doc or "Auto generated doc for {}".format(name)

        def __init__(self):
            super(__class__, self).__init__(name=name, help=help_doc)

        def list_commands(self, ctx):
            return sorted(self.commands.keys())

        def get_command(self, ctx, name):
            if self.commands.get(name) is None:
                self.commands[name] = locator(name)
            return self.commands.get(name)

    return CLI

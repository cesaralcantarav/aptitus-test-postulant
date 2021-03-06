import click
import os

from os.path import expanduser
from cli.utils.config import read_config


config_file = os.path.join(os.path.dirname(__file__), 'config.yaml')
command_folder = os.path.join(os.path.dirname(__file__), 'commands')


class Context(object):
    def __init__(self):
        self.config = read_config(config_file)


pass_context = click.make_pass_decorator(Context, ensure=True)


class cipCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(command_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):

        try:
            ns = {}
            fn = os.path.join(command_folder, name + '.py')
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
            return ns['command']
        except Exception as e:
            click.echo(e)
            return


cli = cipCLI()

@click.command(cls=cipCLI)
@pass_context
def cli(ctx):
   click.echo("Test:Postulant de Aptitus.")
    
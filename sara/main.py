from sara.utils.sara_estrutural import main as main_estrutural
from . import __version__
from docopt import docopt

def cli(args):

    if args['--estrutural']:
        main_estrutural()
    else:
        print("Comando invalido, comando valido sara estrutural")
def main():
    args = docopt(__doc__, version=__version__)
    print(args)
    cli(args)

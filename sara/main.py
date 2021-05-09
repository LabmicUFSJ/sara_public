""" Sara CLI

Usage:
  sara --version
  sara --show-config
  sara -h | --help
  sara -n | --networks <network_name> <collection_name> <directed> <type>

Options:
  --show-config  Show config.
  --version  Show sara version.
  -h --help  Show help file.
  -n --networks  Call module to generate networks; type (r || m).
"""
from sara.utils.sara_estrutural import main as main_network
from . import __version__
from docopt import docopt


def cli(args):
    """CLI commands supported by sara."""
# def main(network_name, collection_name, directed, limit, source):
    if args.get('--networks'):
        # data = args.get('<arg>')
        network_name = args.get('<network_name>')
        collection_name = args.get('<collection_name>')
        directed = args.get('<directed>')
        network_type = args.get('<type>')
        main_network(network_name, collection_name, directed, 0, network_type)
    elif args.get('--version'):
        print(f"Sara Version {__version__}")
    else:
        print("Comando invalido, comando valido sara estrutural")


def main():
    """Get command to run in console."""
    args = docopt(__doc__, version=__version__)
    cli(args)

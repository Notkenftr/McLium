import argparse
from mclium.context import Context


def init_parser():
    parser = argparse.ArgumentParser(
        prog="Mclium",
        description='Minecraft server/client pentest tool'
    )
    subparser = parser.add_subparsers()

    Context().subparser = subparser
    args = parser.parse_args()
    args.func(args)


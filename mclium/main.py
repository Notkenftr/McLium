import argparse
from mclium.context import Context
from mclium.load_plugin import load

def init_parser():
    parser = argparse.ArgumentParser(
        prog="Mclium",
        description="Minecraft server/client pentest tool"
    )

    subparser = parser.add_subparsers(dest="command")
    Context().subparser = subparser

    load()

    args = parser.parse_args()

    if hasattr(args, "_callback"):
        args._callback(args)
    else:
        parser.print_help()


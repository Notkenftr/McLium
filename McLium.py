import argparse
from src import DataBridge
def main():
    parser = argparse.ArgumentParser(
        prog="McLium",
        description="Minecraft server pentest tool",
    )
    subparsers = parser.add_subparsers()

    DataBridge.set_subparser(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
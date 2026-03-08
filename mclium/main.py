import argparse
from mclium.context import Context
from mclium.load_plugin import load

import time
import rich
from rich.console import Console
from rich.prompt import Prompt

def init_parser():
    console = Console()
    console.print(r"    __  ___     __    _               ")
    time.sleep(0.1)
    console.print(r"   /  |/  /____/ /   (_)_  ______ ___ ")
    time.sleep(0.1)
    console.print(r"  / /|_/ / ___/ /   / / / / / __ `__ \.")
    time.sleep(0.1)
    console.print(r" / /  / / /__/ /___/ / /_/ / / / / / /")
    time.sleep(0.1)
    console.print(r"/_/  /_/\___/_____/_/\__,_/_/ /_/ /_/ ")
    time.sleep(0.1)
    console.print("\n")



    parser = argparse.ArgumentParser(
        prog="Mclium",
        description="Minecraft server/client pentest tool"
    )

    subparser = parser.add_subparsers(dest="command")
    Context().subparser = subparser

    load()

    while True:
        try:
            cmd = console.input("[bold cyan]McLium[/bold cyan] > ")

            if cmd in ["exit", "quit"]:
                print("Bye.")
                break

            if not cmd:
                continue

            args = parser.parse_args(cmd.split())

            if hasattr(args, "_callback"):
                args._callback(args)
            else:
                parser.print_help()

        except KeyboardInterrupt:
            print()
            continue

        except Exception as e:
            print("Error:", e)

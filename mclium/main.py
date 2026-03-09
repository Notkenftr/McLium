import argparse
from mclium.context import Context
from mclium.load_plugin import load

import time
from rich.console import Console


def entry_point():
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
    console.print(r"McLium by @kenftr")
    console.print("\n")


    parser = argparse.ArgumentParser(
        prog="Mclium",
        description="Minecraft server/client pentest tool"
    )

    subparser = parser.add_subparsers(dest="command")
    Context().subparser = subparser

    loaded_plugin = load()
    console.print()
    console.print(f"[bold green]Loaded {len(loaded_plugin)} plugins[/bold green]\n")
    for plugin in loaded_plugin:
        console.print(f"[cyan]•[/cyan] {plugin}")
    while True:
        try:
            console.rule()
            console.print("\n")
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
            continue

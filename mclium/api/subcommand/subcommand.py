from abc import ABC, abstractmethod
from mclium.context import Context
from rich.console import Console

class SubCommandModule(ABC):
    def __init__(self, name, flags=None):
        self.name = name
        self.flags = flags or []
        self.subparser = Context().subparser
        self.sub = None
        self.console = Console()

    def register_subcommand(self):
        self.sub = self.subparser.add_parser(self.name)
        for flag in self.flags:
            names = []
            if flag.short:
                names.append(flag.short)
            names.append(flag.long)

            self.sub.add_argument(
                *names,
                dest=flag.dest,
                action=flag.action,
                type=None if flag.action in ("store_true", "store_false") else flag.type,
                default=flag.default,
                required=flag.required,
                help=flag.help
            )

        self.sub.set_defaults(_callback=self._entry)

    def _entry(self, args):
        self.on_command(args)
        self._interactive_loop()

    def _interactive_loop(self):
        while True:
            command = self.console.input(
                f"[bold cyan]McLium[/bold cyan] - (mclium/{self.name}) >> "
            )
            command = command.strip()

            if command in ("exit", "quit"):
                self.console.print("bye. Return to main.")
                break

            if command:
                self.interactive(command)
    @abstractmethod
    def on_command(self, args):
        pass

    def interactive(self, command):
        pass

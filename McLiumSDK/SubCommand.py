import argparse
from src import DataBridge
from typing import Callable

class McLiumCommand:
    def __init__(self, name: str, *flags):
        self.name = name
        self.flags = flags
        self.subcommand_obj: argparse._SubParsersAction = DataBridge.getSubparser()
        self.sub = None
        self._SetupCommand()

    def _SetupCommand(self):
        self.sub = self.subcommand_obj.add_parser(self.name)
        if len(self.flags) > 0:
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
    def setCallback(self, func: Callable):
        self.sub.set_defaults(callback=func)
        return func
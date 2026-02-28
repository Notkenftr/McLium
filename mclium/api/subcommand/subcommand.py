from abc import ABC, abstractmethod
from mclium.context import Context


class SubCommandModule(ABC):
    def __init__(self, name, flags=None):
        self.name = name
        self.flags = flags or []
        self.subparser = Context().subparser
        self.sub = None

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

        self.sub.set_defaults(_callback=self.on_command)

    @abstractmethod
    def on_command(self, args):
        pass

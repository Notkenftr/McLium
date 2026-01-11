class Flag:
    def __init__(
        self,
        short: str | None,
        long: str,
        *,
        dest: str | None = None,
        action: str = "store",
        type=str,
        default=None,
        required: bool = False,
        help: str = ""
    ):
        self.short = short
        self.long = long
        self.dest = dest or long.lstrip("-").replace("-", "_")

        self.action = action
        self.type = type
        self.default = default
        self.required = required
        self.help = help


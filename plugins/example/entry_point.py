from mclium.api import SubCommandModule
from mclium.mclium_types import Flag

class Main(SubCommandModule):
    def __init__(self):
        flags = [
            Flag("-e",
                 "--example",
                 dest="example",
                 type=str,
                 required=True,
                 help="Example command",
                 )
        ]

        super().__init__("example", flags)

    def on_command(self, args):
        print(f"this is example command, your input -> {args.example}")


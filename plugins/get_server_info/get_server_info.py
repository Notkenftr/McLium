from mclium.api import SubCommandModule
from mclium.mclium_types import Flag

class Main(SubCommandModule):
    def __init__(self):
        flags = [
            Flag(
                "-a",
                "--address",
                type=str,
                required=True,
                help="Server address",
            ),
            Flag(
                "-p",
                "--port",
                type=int,
                required=False,
                default=25565,
                help="Server port",
            )
        ]
        super().__init__('get-server-info',flags)

    def on_command(self, args):
        address = args.address
        port = args.port


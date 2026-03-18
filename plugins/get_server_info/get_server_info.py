import socket
from mclium.api.network.mc_protocol import PacketList
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
            ),
            Flag(
                short='-ptc',
                long='--protocol',
                type=int,
                required=False,
                default=774,
            ),
            Flag(
                short='-t',
                long='--timeout',
                type=int,
                required=False,
                default=1,
            )
        ]
        super().__init__('get-server-info',flags)

    def on_command(self, args):
        address = args.address
        port = args.port
        protocol = args.protocol
        timeout = args.timeout

        handshake = PacketList().get_handshake_state(
            protocol=protocol,
            address=address,
            port=port
        )
        status_req = PacketList().get_status_request()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, port))

        sock.sendall(handshake)
        sock.sendall(status_req)
        sock.settimeout(timeout)

        try:
            while True:
                data = sock.recv(1024)
                if not data:
                    continue
                print(data)
        except socket.timeout:
            pass

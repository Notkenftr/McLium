import socket
import threading
import uuid

from mclium.mclium_types import PacketFieldType
from mclium.api import PacketFlow,PacketFieldType,_Field
from mclium.api import PacketList
from mclium.api.network.mc_protocol import Read

class ProtocolSession:
    def __init__(self,
                 address:str,
                 port:int,
                 protocol_version:int,
                 bot_name,
                 timeout=5):
        self.address = address
        self.port = port
        self.protocol_version = protocol_version
        self.bot_name = bot_name

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.port))
        self.sock.settimeout(timeout)

        self.current_packet = None
        self.packet_handler = []

    def _revc(self):
        while True:
            try:
                data = self.sock.recv(16 * 1024 * 1014)

                if not data:
                    break
                self.current_packet = data

                for handler in self.packet_handlers:
                    handler(data)

            except socket.timeout:
                raise "Time out"

    def on_packet_event(self, func):
        self.packet_handlers.append(func)

    def _login(self):
        handshake = PacketList.get_handshake_state(
            protocol=self.protocol_version,
            address=self.address,
            port=self.port,
            state=1
        )


import socket
import threading
import uuid

from mclium.mclium_types import PacketFieldType
from mclium.api.mc_protocol.packet import PacketBuilder, _Field
from mclium.api.mc_protocol.read import Read


class ProtocolSession:

    def __init__(self):
        self.address = None
        self.port = None
        self.protocol = None

        self.sock = None
        self.running = False

        self.bot_name = None

        # packet handlers
        self._packet_handlers = []

        # stream buffer
        self._buffer = b""

        # flags
        self.compress = False
        self.compress_size = 0



    def create_session(self, address, port, protocol):
        self.address = address
        self.port = port
        self.protocol = protocol

    def set_bot_name(self, name):
        self.bot_name = name



    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.port))

        self.running = True

        threading.Thread(target=self._recv_loop, daemon=True).start()

        self._login()



    def _recv_loop(self):
        while self.running:
            data = self.sock.recv(4096)

            if not data:
                continue

            self._buffer += data
            self._handle_stream()



    def _handle_stream(self):

        while True:

            length, size = Read.read_varint(self._buffer)

            if length is None:
                return

            if len(self._buffer) < size + length:
                return

            raw_packet = self._buffer[size:size + length]

            self._buffer = self._buffer[size + length:]

            for handler in self._packet_handlers:
                handler(raw_packet)

    def on_packet(self, func):
        self._packet_handlers.append(func)
        return func


    def send_packet(self, builder: PacketBuilder):
        data = builder.build()
        self.sock.sendall(data)

    def _login(self):

        # login flags
        self.login_success = False
        self.login_acknowledged = False
        self.finish_config = False


        if not self.bot_name:
            raise Exception("Bot name not set")

        handshake = PacketBuilder(0x00, False)

        handshake.add_field(_Field(PacketFieldType.VARINT, self.protocol))
        handshake.add_field(_Field(PacketFieldType.STRING, self.address))
        handshake.add_field(_Field(PacketFieldType.UNSIGNED_SHORT, self.port))
        handshake.add_field(_Field(PacketFieldType.VARINT, 2))

        self.send_packet(handshake)

        _uuid = uuid.uuid3(uuid.NAMESPACE_DNS, f"OfflinePlayer:{self.bot_name}")

        login = PacketBuilder(0x00, False)

        login.add_field(_Field(PacketFieldType.STRING, self.bot_name))
        login.add_field(_Field(PacketFieldType.UUID, _uuid.bytes))

        self.send_packet(login)

        @self.on_packet
        def login_success(packet):
            packet_id, size = Read.read_varint(packet)
            if packet_id != 0x02:
                self.login_success = True
        @self.on_packet
        def set_compress(packet):
            packet_id, size = Read.read_varint(packet)
            if packet_id != 0x03:
                threshold,th_size = Read.read_varint(packet[size:])
                self.compress = True
                self.compress_size = threshold
        if self.login_success:
            login_acknowledged = PacketBuilder(0x03, False)
            self.send_packet(login_acknowledged)
            self.login_acknowledged = True
            finish_config = PacketBuilder(0x02, False)
            self.send_packet(finish_config)
            self.finish_config = True

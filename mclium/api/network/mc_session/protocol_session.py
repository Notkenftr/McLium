import socket
from mclium.api import PacketBuilderWrappedApi
from mclium.api import PacketList
from mclium.api.network.mc_protocol import Read

class ProtocolSession:
    def __init__(self,
                 address:str,
                 port:int,
                 protocol_version:int,
                 bot_name,
                 debug=False,
                 timeout=5):
        self.inject_packet = None
        self.address = address
        self.port = port
        self.protocol_version = protocol_version
        self.bot_name = bot_name
        self.debug = debug

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.port))
        self.sock.settimeout(timeout)

        self.current_packet = None
        self.packet_handlers = []

        self.is_compress = False
        self.compress_size = 0

        self.is_packet_sniffer = False
        self.is_running = False

        self.state = None

    def _recv(self):
        while self.is_running:
            try:
                data = self.sock.recv(4096)

                if not data:
                    continue
                if self.is_packet_sniffer:
                    print("[S->C] {data}".format(data=data))

                for handler in self.packet_handlers:
                    handler(data)

            except socket.timeout:
                continue

    def send_packet(self,packet):
        if self.is_packet_sniffer:
            print("[C->S] {data}".format(data=packet))
        if not self.is_compress:
            self.sock.sendall(packet)
        else:
            packet = PacketBuilderWrappedApi(packet)
            self.sock.sendall(packet.rebuild_with_compressed(self.compress_size))

    def on_packet_event(self, func):
        self.packet_handlers.append(func)

    def _login(self):
        @self.on_packet_event
        def on_packet(packet):
            offset = 0
            buf = packet

            if not self.is_compress:
                length,offset = Read.read_varint(buf,offset)
                packet_id, offset = Read.read_varint(buf, offset)
            else:
                length,offset = Read.read_varint(buf,offset)
                data_length,offset = Read.read_varint(buf, offset)
                remaining = buf[offset: offset + length]

                data_start = offset

                if data_length == 0:
                    inner_buf = buf[data_start:data_start + (length - (data_start))]
                    inner_offset = 0
                    packet_id, inner_offset = Read.read_varint(inner_buf, inner_offset)

                    print(packet)
                    print(packet_id)
                    data_buf = length
                else:
                    import zlib
                    decompressed = zlib.decompress(remaining)
                    inner_offset = 0
                    packet_id, inner_offset = Read.read_varint(decompressed, inner_offset)
                    data_buf = decompressed
                offset = 0

            if packet_id == 0x03:
                threshold, offset = Read.read_varint(buf, offset)
                self.is_compress = True
                self.compress_size = threshold
                print("set compress")

            elif packet_id == 0x02:
                login_acknowedged = PacketList.get_login_acknowledged()
                self.send_packet(login_acknowedged)

        handshake = PacketList.get_handshake_state(
            protocol=self.protocol_version,
            address=self.address,
            port=self.port,
            state=2
        )
        login_start = PacketList.get_login_start(
            name=self.bot_name
        )
        self.send_packet(handshake)
        self.send_packet(login_start)

    def packet_sniffer(self,value):
        if value not in [True, False]:
            raise ValueError("Invalid sniffer value")
        self.is_packet_sniffer = value

    def start(self):
        import threading
        self.is_running = True
        thread = threading.Thread(target=self._recv, daemon=False)
        thread.start()

        self._login()
        thread.join()
if __name__ == '__main__':
    session = ProtocolSession(
        address="localhost",
        port=25565,
        protocol_version=767,
        bot_name="kenftr",
        timeout=10
    )
    session.packet_sniffer(True)
    session.start()

# The login process is as follows:
#
#     C→S: Handshake with intent set to 2 (login) or 3 (transfer)
#     C→S: Login Start
#     S→C: Encryption Request
#     Client auth (if enabled)
#     C→S: Encryption Response
#     Server auth (if enabled)
#     Both enable encryption
#     S→C: Set Compression (optional)
#     S→C: Login Success
#     C→S: Login Acknowledged

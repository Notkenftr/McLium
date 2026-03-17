import socket
from mclium.api import PacketList
from mclium.api.network.mc_protocol import Read

class ProtocolSession:
    def __init__(self,
                 address:str,
                 port:int,
                 protocol_version:int,
                 bot_name,
                 timeout=5):
        self.inject_packet = None
        self.address = address
        self.port = port
        self.protocol_version = protocol_version
        self.bot_name = bot_name

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.port))
        self.sock.settimeout(timeout)

        self.current_packet = None
        self.packet_handlers = []

        self.is_compress = False
        self.compress_size = 0

        self.is_packet_sniffer = False
        self.is_running = False

    def _revc(self):
        while self.is_running:
            try:
                data = self.sock.recv(4096)

                if not data:
                    break

                for handler in self.packet_handlers:
                    handler(data)

            except socket.timeout:
                continue

    def send_packet(self,packet):
        self.sock.sendall(packet)

    def on_packet_event(self, func):
        self.packet_handlers.append(func)

    def _login(self):
        @self.on_packet_event
        def on_packet(packet):
            if not self.is_compress:
                buf = packet
                if self.is_packet_sniffer == True:
                    print("Raw bytes: {buf}".format(buf=buf))
                offset = 0

                length,offset = Read.read_varint(buf,offset)
                packet_id, offset = Read.read_varint(buf,offset)

                if packet_id == 0x03:
                    threshold, offset = Read.read_varint(buf, offset)
                    print("Compression threshold =", threshold)


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
        thread = threading.Thread(target=self._revc, daemon=False)
        thread.start()

        self._login()
        thread.join()


if __name__ == '__main__':
    session = ProtocolSession(
        address="localhost",
        port=25565,
        protocol_version=767,
        bot_name="kenftr",
        timeout=5
    )
    session.packet_sniffer(True)
    session.start()

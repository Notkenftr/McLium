import socket
import threading
import time

from mclium.api import PacketBuilderWrappedApi
from mclium.api import PacketList
from mclium.api.network.mc_protocol import Read
from mclium.api import PacketBuilder
from mclium.api import S2CPacket
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

        self.packet_history = []

        self.current_packet = None
        self.packet_handlers = []

        self.is_compress = False
        self.compress_size = 0

        self.is_packet_sniffer = False
        self.is_running = False

        self.state = "LOGIN"

    def _recv(self):
        while self.is_running:
            try:
                data = self.sock.recv(4096)

                if not data:
                    continue
                if self.is_packet_sniffer:
                    self.packet_history.append(data)
                    print("[S->C] {data}".format(data=data))

                for handler in self.packet_handlers:
                    handler(data)

            except socket.timeout:
                continue

    def send_packet(self, packet):
        if isinstance(packet, PacketBuilder):
            raw = packet.Build()
            if self.is_compress:
                wrapped = PacketBuilderWrappedApi(packet)
                compressed_bytes = wrapped.rebuild_with_compressed(self.compress_size)
                self.sock.sendall(compressed_bytes)

                if self.is_packet_sniffer:
                    self.packet_history.append(packet)
                    print("[C->S] (compressed) {data}".format(data=compressed_bytes))
            else:
                self.sock.sendall(raw)

                if self.is_packet_sniffer:
                    self.packet_history.append(packet)
                    print("[C->S] {data}".format(data=raw))

        elif isinstance(packet, bytes):
            self.sock.sendall(packet)
            if self.is_packet_sniffer:
                self.packet_history.append(packet)
                print("[C->S] {data}".format(data=packet))
        else:
            raise TypeError("Unknown packet type")
    def on_packet_event(self, func):
        self.packet_handlers.append(func)

    def _login(self):
        @self.on_packet_event
        def on_packet(packet):
            global inner_buf, data_buf
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
                    data_buf = inner_buf
                else:
                    import zlib
                    decompressed = zlib.decompress(remaining)
                    inner_offset = 0
                    packet_id, inner_offset = Read.read_varint(decompressed, inner_offset)
                    data_buf = decompressed
                offset = 0


            if self.state == "LOGIN":
                if packet_id == 0x03:
                    threshold, _ = Read.read_varint(buf, offset)
                    self.is_compress = True
                    self.compress_size = threshold

                elif packet_id == 0x02:
                    login_ack = PacketList.get_login_acknowledged(False,False)
                    self.send_packet(login_ack)
                    self.state = "CONFIG"

            elif self.state == "CONFIG":
                if packet_id == 0x04:
                    keep_alive_id,inner_offset = Read.read_varint(data_buf, inner_buf)
                    response = PacketList.get_keepalive(keep_alive_id,False,False)
                    self.send_packet(response)

                elif packet_id == 0x03:
                    finish_ack = b'\x03'
                    self.send_packet(finish_ack)
                    self.state = "PLAY"

                elif packet_id == 0x01:
                    pass

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

    def get_packet_history(self):
        """
        Chỉ hoạt động khi bật packet sniifer
        :return: list
        """
        if self.is_packet_sniffer:
            return self.packet_history
        return []

    def start(self):
        import threading
        self.is_running = True
        thread = threading.Thread(target=self._recv, daemon=False)
        thread.start()

        self._login()
        thread.join()

if __name__ == '__main__':
    from mclium.api.network.fake_server.fake_server import FakeServer

    fake_server = FakeServer(
        "localhost",
        25566
    )

    fake_server.reply_multi_packet(b'\x18\x00\x06kenftr\xfc"\x00\xab=\x073\x7f\x8f\x0e\xb4\xeb\xdc\x98&S',
                                   [
                                       b'\x03\x03\x80\x02',
                                       b'\x1b\x00\x02\xcce2\x88\x9f\xf1>\xf7\x99[2\xc6/_\xcd\xc4\x06kenftr\x00\x01'
                                   ])

    fake_server.reply_multi_packet(b'\x02\x00\x03',
                                   [
                                       b'\x19\x00\x01\x0fminecraft:brand\x06Purpur',
                                       b'\x15\x00\x0c\x01\x11minecraft:vanilla',
                                       b'\x17\x00\x0e\x01\tminecraft\x04core\x041.21',
                                       b'\n\x00\x04\x00\x00\x00\x00\x02;\xf5G'
                                   ])

    t = threading.Thread(target=fake_server.start)
    #t.start()

    session = ProtocolSession(
        address="localhost",
        port=25565,
        protocol_version=767,
        bot_name="kenftr",
        timeout=10
    )
    session.packet_sniffer(True)
    session.start()

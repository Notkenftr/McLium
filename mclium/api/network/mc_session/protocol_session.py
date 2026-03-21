import socket
import threading
import time

from mclium.api import PacketBuilderWrappedApi
from mclium.api import PacketList
from mclium.api.network.mc_protocol import Read
from mclium.api import PacketBuilder
from mclium.api import _Field,PacketFieldType
from mclium.api.network.protocol_entities.S2C import S2CPacket


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
        self.send_after = []
        self.on_start_handle = []
        self.packet_ignore_map = {}
        self.packet_whitelist_map = {}

        self.is_compress = False
        self.compress_size = 0

        self.is_packet_sniffer = False
        self.is_running = False
        self.start_recv_at = 0


        self.state = "LOGIN"

    def _packet_handle(self, data):
        packet_list = []
        offset = 0

        while offset < len(data):
            try:
                packet_length, length_varint_size = Read.read_varint(data, offset)

                if offset + length_varint_size + packet_length > len(data):
                    break

                packet_start = offset + length_varint_size
                packet_end = packet_start + packet_length

                raw_packet = data[packet_start:packet_end]
                packet_list.append(raw_packet)

                offset = packet_end

            except Exception as e:
                print(e)
                break

        return packet_list



    def _recv_packet(self):
        while True:
            try:
                data = self.sock.recv(8*1024*1024)
                if not data:
                    continue
                if self.is_compress:
                    s2c = S2CPacket(data,True,True)
                else:
                    s2c = S2CPacket(data,False,True)

                if self.is_packet_sniffer:
                    print(f"[S2C] packet id: {s2c.packet_id} {"(compressed)" if s2c.get_is_packet_compressed() else "(uncompressed)"} packet length {s2c.packet_length} packet raw: {data}")

                packet_id = s2c.get_packet_id()

                if packet_id in self.packet_whitelist_map:
                    for func in self.packet_whitelist_map[packet_id]:
                        if func in self.packet_handlers:
                            func(s2c)

                if packet_id in self.packet_ignore_map:
                    for func in self.packet_ignore_map[packet_id]:
                        if func in self.packet_handlers:
                            func(s2c)


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
                    print("[C2S] (compressed) {data}".format(data=compressed_bytes))
            else:
                self.sock.sendall(raw)

                if self.is_packet_sniffer:
                    self.packet_history.append(packet)
                    print("[C2S] {data}".format(data=raw))

        elif isinstance(packet, bytes):
            self.sock.sendall(packet)
            if self.is_packet_sniffer:
                self.packet_history.append(packet)
                print("[C2S] {data}".format(data=packet))
        else:
            raise TypeError("Unknown packet type")

    def packet_ignore(self, packet_id):
        def decorator(func):
            self.packet_ignore_map.setdefault(packet_id, []).append(func)
            return func

        return decorator
    def packet_whitelist(self, packet_id):
        if packet_id == 0x14:
            pass
        def decorator(func):
            self.packet_whitelist_map.setdefault(packet_id, []).append(func)
            return func
        return decorator
    def only_packet(self,packet_id,func):
        if packet_id not in self.packet_whitelist_map:
            self.packet_whitelist_map[packet_id] = []
        self.packet_whitelist_map[packet_id].append(func)

    def on_packet_event(self,func):
        self.packet_handlers.append(func)

    def on_start(self,func):
        self.on_start_handle.append(func)

    def _start_login(self):

        @self.on_packet_event
        @self.packet_whitelist(0x03)
        def set_compressed_handle(packet: S2CPacket):
            if self.state == "LOGIN":
                threshold,_ = Read.read_varint(packet.get_payload(),0)
                self.is_compress = True
                self.compress_size = threshold

        @self.on_packet_event
        @self.packet_whitelist(0x02)
        def login_acknowledged_handle(packet: S2CPacket):
            if self.state == "LOGIN":
                login_ack = PacketList.get_login_acknowledged(False, False)
                self.send_packet(login_ack)
                self.state = "CONFIG"

        @self.on_packet_event
        @self.packet_whitelist(0x04)
        def keep_alive_handle(packet: S2CPacket):
            if self.state == "CONFIG":
                payload = packet.get_decompressed_payload() or packet.get_payload()
                offset = 0
                keep_alive_id, offset = Read.read_long(payload, offset)
                response = PacketList.get_keepalive(keep_alive_id, False, False)
                self.send_packet(response)

        @self.on_packet_event
        @self.packet_whitelist(14)
        def client_info_handle(packet: S2CPacket):
            print("trigger id 14")
            if self.state == "CONFIG":
                client_information = PacketBuilder(0x00)
                client_information.add_field(_Field(PacketFieldType.STRING, "en_us"))
                client_information.add_field(_Field(PacketFieldType.BYTE, 12))
                client_information.add_field(_Field(PacketFieldType.VARINT, 0))
                client_information.add_field(_Field(PacketFieldType.BOOL, True))
                client_information.add_field(_Field(PacketFieldType.UNSIGNED_BYTE, 0x7F))
                client_information.add_field(_Field(PacketFieldType.VARINT, 0))
                client_information.add_field(_Field(PacketFieldType.BOOL, False))
                client_information.add_field(_Field(PacketFieldType.BOOL, True))

                client_branch = PacketBuilder(0x2)
                client_branch.add_field(_Field(PacketFieldType.STRING, "minecraft:brand"))
                client_branch.add_field(_Field(PacketFieldType.STRING, "fabric"))

                self.send_packet(client_branch)
                self.send_packet(client_information)


        @self.on_packet_event
        @self.packet_whitelist(3)
        def finish_config_handle(packet: S2CPacket):
            if self.state == "CONFIG":
                finish_ack = PacketList.get_acknowledge_finish_configuration()
                self.send_packet(finish_ack)
                self.state = "PLAY"

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

    def start_session(self):
        import threading
        self.is_running = True
        thread = threading.Thread(target=self._recv_packet, daemon=False)
        thread.start()
        self.start_recv_at = time.time()
        self._start_login()
        thread.join()

if __name__ == '__main__':
    from mclium.api.network.fake_server.fake_server import FakeServer

    # fake_server = FakeServer(
    #     "localhost",
    #     25566
    # )
    # fake_server.reply_multi_packet( b'\x19\x00\x07kenftr_\x93\x8aQ\x8a\xa1\x0eL\x02\xab\xc1\xb5q\x1c\xb1\x0f\xee',
    #                                 [
    #                                     b'\x03\x03\x80\x02',
    #                                     b'\x1c\x00\x02\xb5\x00\xaf\xf4`\x103a\xa0\x90\xfe\xad\xb2Q$=\x07kenftr_\x00\x01'
    #                                 ])
    # fake_server.reply_multi_packet(b'\x02\x00\x03',
    #                                [
    #                                    b'\x19\x00\x01\x0fminecraft:brand\x06Purpur',
    #                                    b'\x15\x00\x0c\x01\x11minecraft:vanilla\x17\x00\x0e\x01\tminecraft\x04core\x041.21'
    #                                ])
    # fake_server.start()

    session = ProtocolSession(
            address="localhost",
            port=25565,
            protocol_version=767,
            bot_name="kenftr_",
            timeout=10
        )
    session.packet_sniffer(True)
    session.start_session()
    #
    # client_information = PacketBuilder(0x00)
    # client_information.add_field(_Field(PacketFieldType.STRING, "en_us"))
    # client_information.add_field(_Field(PacketFieldType.BYTE, 12))
    # client_information.add_field(_Field(PacketFieldType.VARINT, 0))
    # client_information.add_field(_Field(PacketFieldType.BOOL, True))
    # client_information.add_field(_Field(PacketFieldType.UNSIGNED_BYTE, 0x7F))
    # client_information.add_field(_Field(PacketFieldType.VARINT, 0))
    # client_information.add_field(_Field(PacketFieldType.BOOL, False))
    # client_information.add_field(_Field(PacketFieldType.BOOL, True))
    # print(PacketBuilderWrappedApi(client_information).rebuild_with_compressed(256))


# # [C2S] b'\x10\x00\xff\x05\tlocalhostc\xdd\x02'
# # [C2S] b'\x19\x00\x07kenftr_\xf7\xcbM\xe6\x0fj15\x80\x00V\x18\x02\xe2\xe0)'
# # raw data: b'\x03\x03\x80\x02'
# # [S2C] packet id: 3 (uncompressed) packet length 3 packet data: b'\x03\x80\x02'
# # raw data: b'\x1c\x00\x02\xb5\x00\xaf\xf4`\x103a\xa0\x90\xfe\xad\xb2Q$=\x07kenftr_\x00\x01'
# # [S2C] packet id: 2 (compressed) packet length 28 packet data: b'\x02\xb5\x00\xaf\xf4`\x103a\xa0\x90\xfe\xad\xb2Q$=\x07kenftr_\x00\x01'
# # [C2S] (compressed) b'\x02\x00\x03'
# # raw data: b'\x19\x00\x01\x0fminecraft:brand\x06Purpur'
# # [S2C] packet id: 1 (compressed) packet length 25 packet data: b'\x01\x0fminecraft:brand\x06Purpur'
# # raw data: b'\x15\x00\x0c\x01\x11minecraft:vanilla'
# # [S2C] packet id: 12 (compressed) packet length 21 packet data: b'\x0c\x01\x11minecraft:vanilla'
# # raw data: b'\x17\x00\x0e\x01\tminecraft\x04core\x041.21'
# # [S2C] packet id: 14 (compressed) packet length 23 packet data: b'\x0e\x01\tminecraft\x04core\x041.21'
#
#
# # client config: b'\x0f\x00\x00\x05en_us\x0c\x00\x01\x7f\x01\x00\x01'
# # client config: b'\x0f\x00\x00\x05en_us\x0c\x00\x01\x7f\x00\x00\x01'

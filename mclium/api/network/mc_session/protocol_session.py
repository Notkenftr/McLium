import socket
import threading
import time

from mclium.api import PacketBuilderWrappedApi
from mclium.api import PacketList
from mclium.api.network.mc_protocol import Read
from mclium.api import PacketBuilder
from mclium.api.network.entities.S2C import S2CPacket


# api method
# recv
# send_packet
# on_packet_event
# packet sniffer
# start

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
        self.packet_ignore_map = {}
        self.packet_whitelist_map = {}

        self.is_compress = False
        self.compress_size = 0

        self.is_packet_sniffer = False
        self.is_running = False

        self.state = "LOGIN"

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
                    print(f"[S2C] packet id: {s2c.packet_id} {"(compressed)" if s2c.get_is_packet_compressed() else "(uncompressed)"} packet length {s2c.packet_length} packet data: {s2c.get_raw_payload()}")

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
                print(raw)
                print(compressed_bytes)
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


    def _start_login(self):

        @self.on_packet_event
        @self.packet_whitelist(0x03)
        def set_compressed_handle(packet: S2CPacket):
            if self.state == "LOGIN":
                threshold,_ = Read.read_varint(packet.get_payload(),0)
                self.is_compress = True
                self.compress_size = threshold
                print(threshold)

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

        self._start_login()
        thread.join()

if __name__ == '__main__':
    import random
    sessions = [
        ProtocolSession(
            address="localhost",
            port=25565,
            protocol_version=767,
            bot_name=str(random.randint(0, 255)),
            timeout=10
        )
        for _ in range(500)  # số bot
    ]

    t = []

    for session in sessions:
        t.append(threading.Thread(target=session.start_session))

    for i in t:
        i.start()

    # from mclium.api import PacketBuilderWrappedApi
    #
    # packet = PacketList.get_keepalive(49950997, False, False)
    # print(packet.Build())
    # wrapped = PacketBuilderWrappedApi(packet)
    # print(wrapped.rebuild_with_compressed(256))

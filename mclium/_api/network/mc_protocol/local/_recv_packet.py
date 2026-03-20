import socket
from mclium.api.network.entities.S2C import S2CPacket
# def _recv_packet(self):
#     while True:
#         try:
#             data = self.sock.recv(8 * 1024 * 1024)
#             if not data:
#                 continue
#             if self.is_compress:
#                 s2c = S2CPacket(data, True, True)
#             else:
#                 s2c = S2CPacket(data, False, True)
#
#             if self.is_packet_sniffer:
#                 print(
#                     f"[S2C] packet id: {s2c.packet_id} {"(compressed)" if s2c.get_is_packet_compressed() else "(uncompressed)"} packet length {s2c.packet_length} packet data: {s2c.get_raw_payload()}")
#
#             packet_id = s2c.get_packet_id()
#
#             if packet_id in self.packet_whitelist_map:
#                 for func in self.packet_whitelist_map[packet_id]:
#                     if func in self.packet_handlers:
#                         func(s2c)
#
#             if packet_id in self.packet_ignore_map:
#                 for func in self.packet_ignore_map[packet_id]:
#                     if func in self.packet_handlers:
#                         func(s2c)
#
#
#         except socket.timeout:
#             continue

def _recv_packet(self,sock:socket.socket, packet):
    recv_buffer = bytearray()

    while True:
        try:
            data = sock.recv(8*1024*1024)
            if not data:
                continue
            recv_buffer += data

            offset = 0
        except:
            pass

if __name__ == '__main__':
    ...

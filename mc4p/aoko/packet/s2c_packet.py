import zlib
from mc4p.aoko.entities.raw_packet import RawPacket
from mc4p.aoko.utils.read import Read

class S2CPacket(RawPacket):
    """
    This is an API that provides packet parsing from the server. This API only works when it's a single packet,
    so if you have a byte string that's unclear whether it's a single packet or a multipacket, use AokoPacketStream to parse it first.
    """
    def __init__(self,
                 packet_data: bytes,
                 *,
                 auto_parser:bool = True,
                 compressed: bool = False):
        super().__init__(packet_data)
        self.packet_data = packet_data
        self.compressed = compressed

        self.offset = 0
        self.payload_offset = 0
        self.data_length_pos = 0
        self.payload_length_pos = 0

        self.packet_length = 0
        self.data_length = 0

        self.packet_id = 0
        self.payload = b''

        if auto_parser:
            self._parser()

    def reset_offset(self):
        self.offset = 0

    def _parser(self):
        self.offset = 0
        self.payload_offset = 0
        self.packet_length, self.offset = Read.read_varint(self.packet_data, self.offset)
        if self.compressed:
            self.data_length_pos = self.offset
            if self.data_length == 0:
                self.payload_data = self.packet_data[self.offset:]
                self.packet_id, self.payload_offset = Read.read_varint(self.payload_data, 0)
            else:
                compressed_payload = self.packet_data[self.offset: self.offset + self.packet_length]
                self.payload_data = zlib.decompress(compressed_payload)
                self.packet_id, self.payload_offset = Read.read_varint(self.payload_data, 0)
        else:
            self.payload_data = self.packet_data[self.offset:]
            self.packet_id, self.payload_offset = Read.read_varint(self.payload_data, 0)

    def get_data_length(self) -> int:
        return self.data_length
    def get_packet_id(self) -> int:
        return self.packet_id
    def get_packet_length(self) -> int:
        return Read.read_varint(self.packet_data,0)
    def get_raw_payload(self) -> bytes:
        return self.packet_data[self.data_length_pos:]
    def get_raw_packet(self) -> bytes:
        return self.packet_data

if __name__ == '__main__':
    data = b'\x14\x00\x86\x06\rplay.2y2c.orgc\xdd\x02'
    packet = S2CPacket(data,auto_parser=True, compressed=False)
    print(packet.packet_id)

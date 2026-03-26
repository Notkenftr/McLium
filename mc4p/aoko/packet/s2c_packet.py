import zlib
from mc4p.aoko.entities.raw_packet import RawPacket
from mc4p.aoko.utils.read import Read

class S2CPacket(RawPacket):
    def __init__(self,
                 packet_data: bytes,
                 compressed: bool = False):
        super().__init__(packet_data)
        self.packet_data = packet_data
        self.compressed = compressed

        self.offset = 0
        self.data_length_pos = 0
        self.payload_length_pos = 0

        self.packet_length = 0
        self.data_length = 0

        self.packet_id = 0

        self._parser()
        self._parser_packet_id()

    def reset_offset(self):
        self.offset = 0

    def _parser(self):
        if self.compressed:
            self.packet_length,self.offset = Read.read_varint(self.packet_data,self.offset)
            self.data_length_pos = self.offset
            self.data_length,self.offset = Read.read_varint(self.packet_data,self.offset)
            self.reset_offset()
        else:
            self.packet_length,self.offset = Read.read_varint(self.packet_data,self.offset)
            self.data_length_pos = self.offset
            self.reset_offset()

    def _parser_packet_id(self):
        if self.compressed:
            if self.data_length == 0:
                payload = self.packet_data[self.data_length_pos:]
                self.packet_id,_ = Read.read_varint(payload,0)
            else:
                payload = self.packet_data[self.data_length_pos:]
                decompressed_payload = zlib.decompress(payload)
                self.packet_id,_ = Read.read_varint(decompressed_payload, 0)
        else:
            self.packet_id,_ = Read.read_varint(self.packet_data,self.data_length_pos)

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
    packet = S2CPacket(data, compressed=False)
    print(packet.packet_id)

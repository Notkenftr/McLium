import zlib
from mclium.api import Read, Encode, Decode


class S2CPacket:
    def __init__(self, packet: bytes, is_compressed=False, auto_parser=True):
        self.packet = packet
        self.is_compressed = is_compressed

        self.offset = 0
        self.inner_offset = 0
        self.packet_length = None
        self.data_length = None
        self.payload = None
        self.decompressed = None
        self.packet_id = None
        self.packet_data = None

        self.is_packet_compressed = False

        if auto_parser:
            self._parse()

    def _parse(self):
        if not self.is_compressed:
            self.packet_length, self.offset = Read.read_varint(self.packet, self.offset)
            self.payload = self.packet[self.offset:self.offset + self.packet_length]
            self.inner_offset = 0
            self.packet_id, self.inner_offset = Read.read_varint(self.payload, self.inner_offset)
            self.packet_data = self.payload[self.inner_offset:]
        else:
            self.packet_length, self.offset = Read.read_varint(self.packet, self.offset)
            self.data_length, self.offset = Read.read_varint(self.packet, self.offset)
            self.payload = self.packet[self.offset:self.offset + self.packet_length]

            if self.data_length == 0:
                self.inner_offset = 0
                self.packet_id, self.inner_offset = Read.read_varint(self.payload, self.inner_offset)
                self.packet_data = self.payload[self.inner_offset:]
            else:
                self.decompressed = zlib.decompress(self.payload)
                self.inner_offset = 0
                self.is_packet_compressed = True
                self.packet_id, self.inner_offset = Read.read_varint(self.decompressed, self.inner_offset)
                self.packet_data = self.decompressed[self.inner_offset:]

    def get_packet_id(self) -> int:
        """Trả về packet ID"""
        return self.packet_id

    def get_payload(self) -> bytes:
        """Trả về payload, đã giải nén nếu compressed"""
        return self.packet_data

    def get_is_packet_compressed(self) -> bool:
        return self.is_compressed

    def get_raw_payload(self) -> bytes:
        """Trả về payload gốc (compressed nếu có)"""
        return self.payload

    def get_raw_packet(self) -> bytes:
        return self.packet


    def get_decompressed_payload(self) -> bytes | None:
        """Trả về payload đã giải nén nếu compressed, None nếu không nén"""
        return self.decompressed

    def get_packet_length(self) -> int:
        """Trả về chiều dài payload"""
        return self.packet_length

    def get_data_length(self) -> int | None:
        """Trả về độ dài dữ liệu trước khi nén, None nếu non-compressed"""
        return self.data_length

if __name__ == '__main__':
    data = b'\x03\x80\x02'
    packet = S2CPacket(data)

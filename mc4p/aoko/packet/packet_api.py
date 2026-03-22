from mc4p.aoko.packet.field import Field

import io

class AokoPacketApi:
    def __init__(self, packet_id: bytes) -> None:
        self.packet_id = packet_id
        self.field_bytes = bytearray()
        self.packet_data = bytearray()

    def add_field(self, field: bytes):
        self.field_bytes.extend(field)

    def add_field_bytes(self,bytes: bytes):
        self.field_bytes.extend(bytes)

    def build_raw_packet(self):
        self.packet_data = bytearray()

        body = bytearray()
        body.extend(self.packet_id)
        body.extend(self.field_bytes)

        packet_length = Field.varInt(len(body))

        self.packet_data.extend(packet_length)
        self.packet_data.extend(body)

    def get_packet_byte_array(self):
        return self.packet_data

    def get_packet_raw_byte(self):
        return bytes(self.packet_data)

packet = AokoPacketApi(Field.varInt(0x00))
packet.add_field(Field.varInt(0x01))
packet.build_raw_packet()
print(packet.get_packet_raw_byte())


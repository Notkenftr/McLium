import asyncio
from mc4p.aoko.packet.field import AokoFieldBuild

from typing import TYPE_CHECKING
from mc4p.aoko.enums.packet_enum import AokoPacketExtendMode

class AokoHeapPacket:
    def __init__(self,AokoPacket: AokoPacketApi):
        self.aoko_packet = AokoPacket

class AokoPacketApi:
    def __init__(self,
                 packet_id: bytes,
                 call_history: bool = True,
                 extend_mode: AokoPacketExtendMode = AokoPacketExtendMode.BYTEARRAY) -> None:
        self.packet_id = packet_id
        self.extend_mode = extend_mode

        self.hooker = []
        self.is_call_history = call_history
        self.call_history = {}

        if self.extend_mode == AokoPacketExtendMode.BYTEARRAY:
            self.field_bytes = bytearray()
            self.packet_data = bytearray()
        elif self.extend_mode == AokoPacketExtendMode.PLUS:
            self.field = []

    def _log_call(self,method_name,*args,**kwargs):
        if not self.is_call_history:
            return

        if method_name not in self.call_history:
            pass

    def add_field(self, field: bytes):
        if self.extend_mode == AokoPacketExtendMode.BYTEARRAY:
            self.field_bytes.extend(field)
        elif self.extend_mode == AokoPacketExtendMode.PLUS:
            self.field.append(field)

    def add_field_bytes(self,byte: bytes):
        self.field_bytes.extend(byte)

    def get_packet_byte_array(self):
        return self.packet_data

    def get_packet_raw_byte(self):
        return bytes(self.packet_data)

    def clean(self):
        self.packet_id = bytearray()
        self.call_history = {}
        self.field_bytes = []
        self.field = []

    def build_raw_packet(self):
        if self.extend_mode == AokoPacketExtendMode.BYTEARRAY:
            body = self.packet_id + self.field_bytes

        elif self.extend_mode == AokoPacketExtendMode.PLUS:
            body = b''.join([self.packet_id, *self.field])

        packet_length = AokoFieldBuild.varInt(len(body))
        self.packet_data = packet_length + body

if __name__ == '__main__':
    import time
    from mclium.api import PacketFieldType, _Field, PacketBuilder
    start = time.time()
    packet = AokoPacketApi(AokoFieldBuild.varInt(0x00),False,AokoPacketExtendMode.BYTEARRAY)
    for _ in range(1):
        packet.add_field(AokoFieldBuild.varInt(0x01))
        packet.build_raw_packet()
    print("AokoPacketApi")
    print(time.time() - start)


    start = time.time()
    packet = PacketBuilder(0x00)
    for _ in range(1):
        packet.clear()
        packet.add_field(_Field(PacketFieldType.VARINT,1))
        packet.Build()
    print("PacketBuilderApi")
    print(time.time() - start)

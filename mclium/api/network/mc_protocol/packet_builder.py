import zlib
import binascii

from mclium.mclium_types import PacketFieldType
from mclium.api.network.mc_protocol import Read
from mclium.api.network.mc_protocol import Encode
from mclium._api.network.mc_protocol.local._EncodeField import _EncodeField

class PacketBuilderWrappedApi:
    def __init__(self,packet: PacketBuilder):
        self.packet = packet

    def rebuild_with_compressed(self,threshold):
        def _strip_packet_length(packet):
            offset = 0
            _,offset = Read.read_varint(packet,offset)

            return packet[offset:]

        raw_data = _strip_packet_length(self.packet.get_raw_packet())

        if len(raw_data) < threshold:
            data_length = Encode.EncodeVarInt(0)
            body = data_length + raw_data

            packet_length = Encode.EncodeVarInt(len(body))

            return packet_length + body
        else:
            compressed = zlib.compress(raw_data)
            data_length = Encode.EncodeVarInt(len(compressed))
            body = data_length + compressed
            packet_length = Encode.EncodeVarInt(len(body))
            return packet_length + body

class _Field:
    def __init__(
        self,
        field_type: PacketFieldType,
        value=None,
        optional: bool = False
    ):
        self.field_type = field_type
        self.value = value
        self.optional = optional

class PacketBuilder:
    def __init__(self, packet_id=None, debug=False):
        self.packet_id = packet_id
        self.fields = []
        self.debug = debug
        self.raw_byte = None

    def set_packet_id(self, packet_id):
        self.packet_id = packet_id

    def get_raw_packet(self):
        return self.raw_byte

    def add_field(self, field):
        self.fields.append(field)

    def Build(self) -> bytes:
        if self.packet_id is None:
            raise ValueError("Packet ID is not set")
        data = bytearray()

        if self.debug:
            print(f"\n[PacketBuilder] PacketID = {hex(self.packet_id)}")

        data += Encode.EncodeVarInt(self.packet_id)

        for field in self.fields:
            data += _EncodeField(field, self.debug)

        packet = Encode.EncodeVarInt(len(data)) + data

        if self.debug:
            print("[PacketBuilder] Raw Packet:", binascii.hexlify(packet).decode())
        self.raw_byte = packet
        return packet


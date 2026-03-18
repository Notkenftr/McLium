import zlib
import hashlib
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

        # packet info
        self.packet_id = packet_id
        self.length = 0
        self.fields = []
        self.fields_length = []
        self.raw_byte = None


        self.debug = debug


    #getter / setter

    def get_packet_id(self) -> int:
        return self.packet_id

    def get_raw_packet(self) -> bytes:
        return self.raw_byte

    def get_fields(self) -> list[_Field]:
        return self.fields

    def get_length(self) -> int:
        return self.length

    def get_fields_length(self) -> list:
        return self.fields_length

    def set_packet_id(self, packet_id):
        self.packet_id = packet_id

    def set_debug(self,value):
        if value not in [True, False]:
            raise ValueError("Debug must be True or False")
        self.debug = value

    # insert
    def insert_byte(self, index: int, value: int):
        if self.raw_byte is None:
            raise ValueError("Packet not built yet")

        if not (0 <= value <= 255):
            raise ValueError("Bytes must be between 0 and 255")

        data = bytearray(self.raw_byte)

        if index < 0 or index > len(data):
            raise IndexError("Index out of range")

        data.insert(index, value)

        offset = 0
        _, offset = Read.read_varint(data, offset)

        body = data[offset:]

        new_packet = Encode.EncodeVarInt(len(body)) + body

        self.raw_byte = new_packet
        return new_packet

    # add

    def add_field(self, field):
        self.fields.append(field)

    def add_fields(self,fields):
        self.fields.extend(fields)

    def add_raw_byte_field(self, raw: bytes):
        self.fields.append(raw)
        return self

    # clear
    def clear(self):
        self.fields.clear()
        self.fields_length.clear()
        self.raw_byte = None
        self.length = 0

    # write
    def write_varint(self, value):
        return self.add_field(_Field(PacketFieldType.VARINT, value))

    def write_string(self, value):
        return self.add_field(_Field(PacketFieldType.STRING, value))

    def write_bool(self, value):
        return self.add_field(_Field(PacketFieldType.BOOL, value))

    # utils
    def pretty(self):
        print(f"PacketID: {hex(self.packet_id)}")
        for i, field in enumerate(self.fields):
            print(f"[{i}] {field}")

    def hex(self):
        if self.raw_byte:
            return self.raw_byte.hex()
        return None

    def size(self):
        return len(self.raw_byte) if self.raw_byte else 0

    def md5(self):
        if self.raw_byte:
            return hashlib.md5(self.raw_byte).hexdigest()

    def diff(self, other):
        return self.raw_byte != other.raw_byte

    # build

    def build_no_length(self) -> bytes:
        data = bytearray()
        data += Encode.EncodeVarInt(self.packet_id)

        for field in self.fields:
            data += _EncodeField(field, self.debug)

        return data

    def Build(self) -> bytes:
        if self.packet_id is None:
            raise ValueError("Packet ID is not set")
        data = bytearray()

        if self.debug:
            print(f"\n[PacketBuilder] PacketID = {hex(self.packet_id)}")

        data += Encode.EncodeVarInt(self.packet_id)

        for field in self.fields:
            _field = _EncodeField(field, self.debug)
            data += _field
            self.fields_length.append(_field)

        packet = Encode.EncodeVarInt(len(data)) + data
        self.length = len(packet)

        if self.debug:
            print("[PacketBuilder] Raw Packet:", binascii.hexlify(packet).decode())
        self.raw_byte = packet
        return packet

    async def async_diff(self,other):
        return self.raw_byte != other.raw_byte

    async def async_build_no_length(self) -> bytes:
        data = bytearray()
        data += Encode.EncodeVarInt(self.packet_id)

        for field in self.fields:
            data += _EncodeField(field, self.debug)

        return data

    async def async_build(self):
        if self.packet_id is None:
            raise ValueError("Packet ID is not set")
        data = bytearray()

        if self.debug:
            print(f"\n[PacketBuilder] PacketID = {hex(self.packet_id)}")

        data += Encode.EncodeVarInt(self.packet_id)

        for field in self.fields:
            _field = _EncodeField(field, self.debug)
            data += _field
            self.fields_length.append(_field)

        packet = Encode.EncodeVarInt(len(data)) + data
        self.length = len(packet)

        if self.debug:
            print("[PacketBuilder] Raw Packet:", binascii.hexlify(packet).decode())
        self.raw_byte = packet
        return packet

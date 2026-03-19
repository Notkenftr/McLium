import zlib
import hashlib
import binascii

from enum import Enum
from mclium.mclium_types import PacketFieldType
from mclium.api.network.mc_protocol import Read
from mclium.api.network.mc_protocol import Encode
from mclium.api.network.mc_protocol.build_hook_at import BuildHookAt
from mclium._api.network.mc_protocol.local._EncodeField import _EncodeField
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

class PacketBuilderWrappedApi:
    def __init__(self,packet: PacketBuilder):
        self.packet = packet

    def rebuild_with_compressed(self, threshold):
        from mclium.api.network.mc_protocol import Encode
        import zlib

        raw_data = self.packet.build_no_length()

        if threshold <= 0 or len(raw_data) < threshold:
            data_length = Encode.EncodeVarInt(0)
            body = data_length + raw_data

        else:

            compressed = zlib.compress(raw_data)
            data_length = Encode.EncodeVarInt(len(raw_data))

            body = data_length + compressed

        packet_length = Encode.EncodeVarInt(len(body))

        return packet_length + body



    def fake_data_length(self,length:int):
        def _strip_packet_length(packet):
            offset = 0
            _,offset = Read.read_varint(packet,offset)

            return packet[offset:]

        raw_data = _strip_packet_length(self.packet.get_raw_packet())
        return Encode.EncodeVarInt(length) + raw_data

class PacketBuilder:
    """
    First, đây là api giúp build packet, cái này đưa cho bạn 99% control từ craft v.v edit từng byte. Nên hãy cẩn thận vì sai 1 byte hay gì đấy
    có thể làm server crash hoặc bạn sẽ bị kick

    """
    def __init__(self, packet_id=None, debug=False):

        # packet info
        self.packet_id = packet_id
        self.length = 0
        self.fields = []
        self.fields_length = []
        self.raw_byte = None

        #hooker
        self.before_build = []
        self.before_field_add = []
        self.after_field_add = []
        self.before_length_encode = []
        self.after_length_encode = []
        self.after_build = []

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

    def get_bytearrays(self):
        return bytearray(self.raw_byte)

    def set_packet_id(self, packet_id):
        self.packet_id = packet_id

    def set_debug(self,value):
        if value not in [True, False]:
            raise ValueError("Debug must be True or False")
        self.debug = value

    # build hook

    def set_hooker(self, func, at: BuildHookAt):
        if at == BuildHookAt.BEFORE_BUILD:
            self.before_build.append(func)

        elif at == BuildHookAt.BEFORE_FIELD_ADD:
            self.before_field_add.append(func)

        elif at == BuildHookAt.AFTER_FIELD_ADD:
            self.after_field_add.append(func)

        elif at == BuildHookAt.BEFORE_LENGTH_ENCODE:
            self.before_length_encode.append(func)

        elif at == BuildHookAt.AFTER_LENGTH_ENCODE:
            self.after_length_encode.append(func)

        elif at == BuildHookAt.AFTER_BUILD:
            self.after_build.append(func)

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

    # fast write
    def write_varint(self, value):
        return self.add_field(_Field(PacketFieldType.VARINT, value))
    def write_string(self, value):
        return self.add_field(_Field(PacketFieldType.STRING, value))
    def write_long(self,value):
        return self.add_field(_Field(PacketFieldType.LONG, value))
    def write_int(self,value):
        return self.add_field(_Field(PacketFieldType.INT, value))
    def write_unsigned_short(self,value):
        return self.add_field(_Field(PacketFieldType.UNSIGNED_SHORT,value))
    def write_uuid(self,value):
        return self.add_field(_Field(PacketFieldType.UUID, value))
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

        for hook in self.before_build:
            hook(self)

        data = bytearray()

        if self.debug:
            print(f"\n[PacketBuilder] PacketID = {hex(self.packet_id)}")

        data += Encode.EncodeVarInt(self.packet_id)

        for field in self.fields:
            for hook in self.before_field_add:
                hook(self, field)

            _field = _EncodeField(field, self.debug)

            for hook in self.after_field_add:
                hook(self, field, _field)

            data += _field
            self.fields_length.append(_field)

        for hook in self.before_length_encode:
            hook(self, data)

        packet = Encode.EncodeVarInt(len(data)) + data
        self.length = len(packet)

        for hook in self.after_length_encode:
            hook(self, packet)

        if self.debug:
            print("[PacketBuilder] Raw Packet:", binascii.hexlify(packet).decode())

        self.raw_byte = packet

        for hook in self.after_build:
            hook(self, packet)

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

        for hook in self.before_build:
            hook(self)

        data = bytearray()

        if self.debug:
            print(f"\n[PacketBuilder] PacketID = {hex(self.packet_id)}")

        data += Encode.EncodeVarInt(self.packet_id)

        for field in self.fields:
            for hook in self.before_field_add:
                hook(self, field)

            _field = _EncodeField(field, self.debug)

            for hook in self.after_field_add:
                hook(self, field, _field)

            data += _field
            self.fields_length.append(_field)

        for hook in self.before_length_encode:
            hook(self, data)

        packet = Encode.EncodeVarInt(len(data)) + data
        self.length = len(packet)

        for hook in self.after_length_encode:
            hook(self, packet)

        if self.debug:
            print("[PacketBuilder] Raw Packet:", binascii.hexlify(packet).decode())

        self.raw_byte = packet

        for hook in self.after_build:
            hook(self, packet)

        return packet

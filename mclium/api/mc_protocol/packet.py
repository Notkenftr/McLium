from mclium.mclium_types import PacketFieldType
from mclium.api.mc_protocol import Encode

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

def _EncodeField(self, field: "PacketFieldType") -> bytes:
    if field.optional:
        if field.value is None:
            return Encode.EncodeBool(False)
        prefix = Encode.EncodeBool(True)
    else:
        prefix = b""

    ft = field.field_type

    if ft == PacketFieldType.VARINT:
        return prefix + Encode.EncodeVarInt(field.value)

    if ft == PacketFieldType.STRING:
        return prefix + Encode.EncodeString(field.value)

    if ft == PacketFieldType.BOOL:
        return prefix + Encode.EncodeBool(field.value)

    if ft == PacketFieldType.INT:
        return prefix + field.value.to_bytes(4, "big", signed=True)

    if ft == PacketFieldType.UUID:
        if isinstance(field.value, bytes):
            if len(field.value) != 16:
                raise ValueError("UUID must be 16 bytes")
            return prefix + field.value

        import uuid
        if isinstance(field.value, uuid.UUID):
            return prefix + field.value.bytes

        raise TypeError("UUID field must be uuid.UUID or 16-byte bytes")

    raise ValueError(f"Unsupported field type: {ft}")

class PacketBuilder:
    def __init__(self,
                 packet_id = None):
        self.packet_id = packet_id
        self.fields = []

    def set_packet_id(self, packet_id):
        self.packet_id = packet_id

    def add_field(self, field):
        self.fields.append(field)
    def Build(self) -> bytes:
        data = bytearray()
        data += Encode.EncodeVarInt(self.packet_id)

        for field in self.fields:
            data += self.EncodeField(field)

        return Encode.EncodeVarInt(len(data)) + data


class Packet:

    @staticmethod
    def get_handshake_state(protocol,address,port,state = 1):
        packet = PacketBuilder(0x00)
        packet.add_field(_Field(PacketFieldType.VARINT, int(protocol)))
        packet.add_field(_Field(PacketFieldType.STRING, str(address)))
        packet.add_field(_Field(PacketFieldType.INT, int(port)))
        packet.add_field(_Field(PacketFieldType.VARINT, state))


    @staticmethod
    def get_login_start(name: str, player_uuid: str = None) -> bytes:
        import uuid

        if player_uuid is None:
            player_uuid = uuid.uuid3(
                uuid.NAMESPACE_DNS,
                f"OfflinePlayer:{name}"
            ).bytes

        packet = PacketBuilder(0x00)
        packet.add_field(_Field(PacketFieldType.STRING, str(name)))
        packet.add_field(_Field(PacketFieldType.UUID, player_uuid))

        return packet.Build()

    @staticmethod
    def get_status_request():
        packet = PacketBuilder(0x01)
        return packet.Build()

from McLiumSDK import McLium
from McLiumSDK.Types import FieldType
class PacketBuilder:
    def __init__(self, packet_id: int):
        self.packet_id = packet_id
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)
        return self

    class Field:
        def __init__(
            self,
            field_type: FieldType,
            value=None,
            optional: bool = False
        ):
            self.field_type = field_type
            self.value = value
            self.optional = optional
    def EncodeField(self, field: "PacketBuilder.Field") -> bytes:
        if field.optional:
            if field.value is None:
                return McLium.McProtocol.EncodeBool(False)
            prefix = McLium.McProtocol.EncodeBool(True)
        else:
            prefix = b""

        ft = field.field_type

        if ft == FieldType.VARINT:
            return prefix + McLium.McProtocol.EncodeVarInt(field.value)

        if ft == FieldType.STRING:
            return prefix + McLium.McProtocol.EncodeString(field.value)

        if ft == FieldType.BOOL:
            return prefix + McLium.McProtocol.EncodeBool(field.value)

        if ft == FieldType.INT:
            return prefix + field.value.to_bytes(4, "big", signed=True)

        raise ValueError(f"Unsupported field type: {ft}")

    def Build(self) -> bytes:
        data = bytearray()
        data += McLium.McProtocol.EncodeVarInt(self.packet_id)

        for field in self.fields:
            data += self.EncodeField(field)

        return McLium.McProtocol.EncodeVarInt(len(data)) + data

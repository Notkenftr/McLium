from mclium.mclium_types import PacketFieldType
from mclium.api.network.mc_protocol import Encode
def _EncodeField(field: "PacketFieldType", debug=False) -> bytes:
    if field.optional:
        if field.value is None:
            if debug:
                print("[Field] Optional = False")
            return Encode.EncodeBool(False)
        prefix = Encode.EncodeBool(True)
    else:
        prefix = b""

    ft = field.field_type

    if debug:
        print(f"[Field] Type={ft} Value={field.value}")

    if ft == PacketFieldType.VARINT:
        return prefix + Encode.EncodeVarInt(field.value)

    if ft == PacketFieldType.STRING:
        return prefix + Encode.EncodeString(field.value)

    if ft == PacketFieldType.BOOL:
        return prefix + Encode.EncodeBool(field.value)

    if ft == PacketFieldType.INT:
        return prefix + field.value.to_bytes(4, "big", signed=True)

    if ft == PacketFieldType.UNSIGNED_SHORT:
        return prefix + field.value.to_bytes(2, "big")
    if ft == PacketFieldType.LONG:
        return prefix + field.value.to_bytes(8, "big", signed=True)
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

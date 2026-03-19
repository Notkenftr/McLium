class Encode:

    @staticmethod
    def EncodeVarInt(value: int) -> bytes:
        result = bytearray()
        value &= 0xFFFFFFFF

        while True:
            temp = value & 0x7F
            value >>= 7
            if value != 0:
                temp |= 0x80
            result.append(temp)
            if value == 0:
                break
        return bytes(result)

    @staticmethod
    def EncodeVarLong(value: int) -> bytes:
        result = bytearray()
        value &= 0xFFFFFFFFFFFFFFFF

        while True:
            temp = value & 0x7F
            value >>= 7
            if value != 0:
                temp |= 0x80
            result.append(temp)
            if value == 0:
                break
        return bytes(result)

    @staticmethod
    def EncodeString(string: str) -> bytes:
        string_bytes = string.encode("utf-8")
        return Encode.EncodeVarInt(len(string_bytes)) + string_bytes

    @staticmethod
    def EncodeBool(value: bool) -> bytes:
        return b'\x01' if value else b'\x00'

    @staticmethod
    def EncodeByte(value: int) -> bytes:
        return value.to_bytes(1, "big", signed=True)

    @staticmethod
    def EncodeUnsignedByte(value: int) -> bytes:
        return value.to_bytes(1, "big", signed=False)

    @staticmethod
    def EncodeShort(value: int) -> bytes:
        return value.to_bytes(2, "big", signed=True)

    @staticmethod
    def EncodeUnsignedShort(value: int) -> bytes:
        return value.to_bytes(2, "big", signed=False)

    @staticmethod
    def EncodeInt(value: int) -> bytes:
        return value.to_bytes(4, "big", signed=True)

    @staticmethod
    def EncodeLong(value: int) -> bytes:
        return value.to_bytes(8, "big", signed=True)

    @staticmethod
    def EncodeFloat(value: float) -> bytes:
        import struct
        return struct.pack(">f", value)

    @staticmethod
    def EncodeDouble(value: float) -> bytes:
        import struct
        return struct.pack(">d", value)

    @staticmethod
    def EncodeUUID(value) -> bytes:
        import uuid
        if isinstance(value, uuid.UUID):
            return value.bytes
        elif isinstance(value, bytes) and len(value) == 16:
            return value
        else:
            raise TypeError("UUID must be uuid.UUID or 16-byte bytes")

    @staticmethod
    def EncodeByteArray(data: bytes) -> bytes:
        return Encode.EncodeVarInt(len(data)) + data

    @staticmethod
    def EncodeLongArray(data: list[int]) -> bytes:
        result = Encode.EncodeVarInt(len(data))
        for v in data:
            result += Encode.EncodeLong(v)
        return result

    @staticmethod
    def EncodeIntArray(data: list[int]) -> bytes:
        result = Encode.EncodeVarInt(len(data))
        for v in data:
            result += Encode.EncodeInt(v)
        return result

    @staticmethod
    def EncodePosition(x: int, y: int, z: int) -> bytes:
        value = ((x & 0x3FFFFFF) << 38) | ((z & 0x3FFFFFF) << 12) | (y & 0xFFF)
        return value.to_bytes(8, "big", signed=True)

    @staticmethod
    def EncodeAngle(value: float) -> bytes:
        return int(value * 256 / 360) & 0xFF

    @staticmethod
    def EncodeNBT(data: bytes) -> bytes:
        return data

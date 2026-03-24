from mc4p.aoko import Encode

class AokoFieldBuild:
    @staticmethod
    def varInt(value: int) -> bytes:
        return Encode.EncodeVarInt(value)

    @staticmethod
    def varLong(value: int) -> bytes:
        return Encode.EncodeVarLong(value)

    @staticmethod
    def string(value: str) -> bytes:
        return Encode.EncodeString(value)

    @staticmethod
    def byte_array(data: bytes) -> bytes:
        return Encode.EncodeByteArray(data)

    @staticmethod
    def long_array(data: list[int]) -> bytes:
        return Encode.EncodeLongArray(data)

    @staticmethod
    def int_array(data: list[int]) -> bytes:
        return Encode.EncodeIntArray(data)

    @staticmethod
    def byte(value: int) -> bytes:
        return Encode.EncodeByte(value)

    @staticmethod
    def unsigned_byte(value: int) -> bytes:
        return Encode.EncodeUnsignedByte(value)

    @staticmethod
    def short(value: int) -> bytes:
        return Encode.EncodeShort(value)

    @staticmethod
    def unsigned_short(value: int) -> bytes:
        return Encode.EncodeUnsignedShort(value)

    @staticmethod
    def int(value: int) -> bytes:
        return Encode.EncodeInt(value)

    @staticmethod
    def long(value: int) -> bytes:
        return Encode.EncodeLong(value)

    @staticmethod
    def float(value: float) -> bytes:
        return Encode.EncodeFloat(value)

    @staticmethod
    def double(value: float) -> bytes:
        return Encode.EncodeDouble(value)

    @staticmethod
    def boolean(value: bool) -> bytes:
        return Encode.EncodeBool(value)

    @staticmethod
    def uuid(value) -> bytes:
        return Encode.EncodeUUID(value)

    @staticmethod
    def position(x: int, y: int, z: int) -> bytes:
        return Encode.EncodePosition(x, y, z)

    @staticmethod
    def angle(value: float) -> bytes:
        res = Encode.EncodeAngle(value)
        return res.to_bytes(1, "big")

    @staticmethod
    def nbt(data: bytes) -> bytes:
        return Encode.EncodeNBT(data)

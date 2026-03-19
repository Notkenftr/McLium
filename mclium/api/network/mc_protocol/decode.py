class Decode:
    @staticmethod
    def DecodeVarInt(data: bytes) -> tuple[int, int]:
        num = 0
        shift = 0
        pos = 0

        while True:
            if pos >= len(data):
                raise EOFError("Not enough bytes for VarInt")

            b = data[pos]
            pos += 1

            num |= (b & 0x7F) << shift

            if not (b & 0x80):
                break

            shift += 7
            if shift > 35:
                raise ValueError("VarInt too big")

        return num, pos

    @staticmethod
    def DecodeString(data: bytes) -> tuple[str, int]:
        from mclium.api import Encode
        length, offset = Encode.DecodeVarInt(data)

        end = offset + length
        if end > len(data):
            raise EOFError("Not enough bytes for String")

        string = data[offset:end].decode("utf-8")
        return string, end

    @staticmethod
    def DecodeBool(data: bytes) -> tuple[bool, int]:
        if len(data) < 1:
            raise EOFError("Not enough bytes for Boolean")
        return data[0] != 0, 1

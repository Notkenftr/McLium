class Encode:
    @staticmethod
    def EncodeString(string):
        from mclium.api.network.mc_protocol import Encode
        string_bytes = string.encode('utf-8')
        return Encode.EncodeVarInt(len(string_bytes)) + string_bytes

    @staticmethod
    def EncodeVarInt(value: int):
        result = bytearray()
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
    def EncodeBool(value: bool) -> bytes:
        return b'\x01' if value else b'\x00'


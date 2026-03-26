class Read:

    @staticmethod
    def read_varint(data: bytes, offset: int = 0):
        num = 0
        shift = 0

        for i in range(5):
            if offset >= len(data):
                raise ValueError("Out of bounds while reading VarInt")

            byte = data[offset]
            offset += 1

            num |= (byte & 0x7F) << shift

            if not (byte & 0x80):
                return num, offset

            shift += 7

        raise ValueError("VarInt too big")

    @staticmethod
    def read_long(data: bytes, offset: int = 0):
        import struct
        if offset + 8 > len(data):
            raise ValueError("Not enough bytes to read a Long")

        value = struct.unpack('>q', data[offset:offset + 8])[0]
        offset += 8
        return value, offset

    @staticmethod
    def read_string(data: bytes, offset: int = 0):
        length, offset = Read.read_varint(data, offset)

        if offset + length > len(data):
            raise ValueError("String out of bounds")

        string_bytes = data[offset:offset + length]
        offset += length

        return string_bytes.decode(), offset

class SockRead:
    @staticmethod
    def read_varint(sock):
        num = 0
        for i in range(5):
            byte = sock.recv(1)
            if not byte:
                raise ConnectionError("Disconnected")
            val = byte[0]
            num |= (val & 0x7F) << (7 * i)
            if not (val & 0x80):
                return num
        raise ValueError("VarInt too big")
    @staticmethod
    def read_string(sock):
        length = SockRead.read_varint(sock)
        data = b""
        while len(data) < length:
            data += sock.recv(length - len(data))
        return data.decode()

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
    def read_string(data: bytes, offset: int = 0):
        length, offset = Read.read_varint(data, offset)

        if offset + length > len(data):
            raise ValueError("String out of bounds")

        string_bytes = data[offset:offset + length]
        offset += length

        return string_bytes.decode(), offset

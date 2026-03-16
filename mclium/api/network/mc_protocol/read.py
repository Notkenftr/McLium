class Read:
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
        length = Read.read_varint(sock)
        data = b""
        while len(data) < length:
            data += sock.recv(length - len(data))
        return data.decode()

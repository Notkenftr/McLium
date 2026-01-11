import McLium
class Parser:
    def __init__(self,packet):
        self.packet: bytes = packet

    def getId(self):
        reader = McLium.McProtocol.Decoder(self.packet)
        return reader
    
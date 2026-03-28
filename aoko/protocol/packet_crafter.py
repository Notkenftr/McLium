class AokoPacketCrafter:
    def __init__(self,reset=False):
        self.reset = reset
        self.fields = bytearray()
        self.packet_data = bytearray()
        self.payload = b''


class AokoPacketStream:
    def __init__(self,data):
        self.data = data

        self.offset = 0
        self.packet_list = []
        self.corrupted_packet = []



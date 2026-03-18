import socket
class PacketFlow:

    def __init__(self, debug=False):
        self.packet_list = []
        self.debug = debug

    def add_packet(self, packet):
        self.packet_list.append(packet)

    def send(self, address, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.debug:
            print(f"[PacketFlow] Connecting -> {address}:{port}")

        sock.connect((address, port))

        count = 0

        for packet in self.packet_list:
            sock.sendall(packet)

            if self.debug:
                count += 1
                print(f"[PacketFlow] Sent packet #{count}")
                print("HEX:", packet.hex())

        if self.debug:
            print("[PacketFlow] Done sending packets")

        sock.close()

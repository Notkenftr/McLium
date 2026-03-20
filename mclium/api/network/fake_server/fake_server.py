import time
import socket
class FakeServer:
    def __init__(self,
                 address,
                 port):
        self.address = address
        self.port = port

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind((self.address, self.port))
        self.server_sock.listen(5)
        self.workflow = []
        self.auto_reply = {}
        self.auto_reply_multi_packet = {}
    def add_func_workflow(self,func):
        self.workflow.append(func)
    def reply_single_packet(self,trigger,reply_data):
        self.auto_reply[trigger] = reply_data
    def reply_multi_packet(self,trigger,reply_data: list):
        self.auto_reply_multi_packet[trigger] = reply_data
    def handle_client(self, client_sock, client_addr):
        while True:
            try:
                data = client_sock.recv(8*1024*1024)
                if not data:
                    break
                print(data)

                if data in self.auto_reply:
                    reply = self.auto_reply[data]
                    client_sock.sendall(reply)
                if data in self.auto_reply_multi_packet:
                    for pkt in self.auto_reply_multi_packet[data]:
                        client_sock.sendall(pkt)
                        time.sleep(0.05)

                for func in self.workflow:
                    func(client_sock, data)

            except ConnectionResetError:
                break

        client_sock.close()

    def _host(self):
        import threading
        while True:
            client_sock, client_addr = self.server_sock.accept()
            t = threading.Thread(target=self.handle_client, args=(client_sock, client_addr))
            t.start()

    def start(self):
        self._host()

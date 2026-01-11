from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import socket

def ReadSocket(sock: Optional["socket.socket"]) -> None:
    bytes = b''
    sock.settimeout(0.3)
    while True:
        data = sock.recv(1024)
        if not data:
            continue
        bytes += data

    return bytes

from abc import ABC, abstractmethod

class RawPacket(ABC):
    def __init__(self, packet_data: bytes):
        self.packet_data = packet_data

    @abstractmethod
    def get_packet_length(self) -> int:
        pass

    @abstractmethod
    def get_data_length(self) -> int:
        pass

    @abstractmethod
    def get_raw_packet(self) -> bytes:
        pass

    @abstractmethod
    def get_packet_id(self) -> int:
        pass

    @abstractmethod
    def get_raw_payload(self) -> bytes:
        pass

import socket
import binascii

from mclium.mclium_types import PacketFieldType
from mclium.api.network.mc_protocol import Encode


class _Field:
    def __init__(
        self,
        field_type: PacketFieldType,
        value=None,
        optional: bool = False
    ):
        self.field_type = field_type
        self.value = value
        self.optional = optional


def _EncodeField(field: "PacketFieldType", debug=False) -> bytes:
    if field.optional:
        if field.value is None:
            if debug:
                print("[Field] Optional = False")
            return Encode.EncodeBool(False)
        prefix = Encode.EncodeBool(True)
    else:
        prefix = b""

    ft = field.field_type

    if debug:
        print(f"[Field] Type={ft} Value={field.value}")

    if ft == PacketFieldType.VARINT:
        return prefix + Encode.EncodeVarInt(field.value)

    if ft == PacketFieldType.STRING:
        return prefix + Encode.EncodeString(field.value)

    if ft == PacketFieldType.BOOL:
        return prefix + Encode.EncodeBool(field.value)

    if ft == PacketFieldType.INT:
        return prefix + field.value.to_bytes(4, "big", signed=True)

    if ft == PacketFieldType.UNSIGNED_SHORT:
        return prefix + field.value.to_bytes(2, "big")
    if ft == PacketFieldType.LONG:
        return prefix + field.value.to_bytes(8, "big", signed=True)
    if ft == PacketFieldType.UUID:
        if isinstance(field.value, bytes):
            if len(field.value) != 16:
                raise ValueError("UUID must be 16 bytes")
            return prefix + field.value

        import uuid
        if isinstance(field.value, uuid.UUID):
            return prefix + field.value.bytes

        raise TypeError("UUID field must be uuid.UUID or 16-byte bytes")

    raise ValueError(f"Unsupported field type: {ft}")


class PacketBuilder:
    def __init__(self, packet_id=None, debug=False):
        self.packet_id = packet_id
        self.fields = []
        self.debug = debug

    def set_packet_id(self, packet_id):
        self.packet_id = packet_id

    def add_field(self, field):
        self.fields.append(field)

    def Build(self) -> bytes:
        if self.packet_id is None:
            raise ValueError("Packet ID is not set")
        data = bytearray()

        if self.debug:
            print(f"\n[PacketBuilder] PacketID = {hex(self.packet_id)}")

        data += Encode.EncodeVarInt(self.packet_id)

        for field in self.fields:
            data += _EncodeField(field, self.debug)

        packet = Encode.EncodeVarInt(len(data)) + data

        if self.debug:
            print("[PacketBuilder] Raw Packet:", binascii.hexlify(packet).decode())

        return packet




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

from aoko.enums.packet import AokoPacketFieldType
from aoko.codecs.encode import Encode
from aoko.entities.aoko_field import AokoField
from aoko.codecs.field_encode import _encode_field

class AokoPacketCrafter:
    def __init__(self,auto_reset: bool =False,debug: bool = False):


        self.reset = auto_reset
        self.debug = debug
        self.fields = bytearray()
        self.full_packet_data = bytearray()

        self.packet_length = b''
        self.packet_id = None
        self.packet_body = bytearray()
        self.payload = b''

        self.fields: list[bytes] = []


    def add_field(self,field:AokoField) -> None:
        self.fields.append(field)

    def add_fields(self,fields: list[AokoField]) -> None:
        self.fields.extend(fields)

    def add_raw_field(self,byte: bytes) -> None:
        self.fields.append(byte)

    def set_packet_id(self,id) -> None:
        self.packet_id = id

    def build_no_packet_length(self):
        pass

    def build_normal(self):
        self.payload = bytearray()

        for field in self.fields:
            if isinstance(field,AokoField):
                self.payload.extend(_encode_field(field))

            else:
                self.payload.extend(field)

        self.packet_body.extend(Encode.EncodeVarInt(self.packet_id))
        self.packet_body.extend(self.payload)

        self.packet_length = Encode.EncodeVarInt(len(self.packet_body))

        self.full_packet_data.extend(self.packet_length)
        self.full_packet_data.extend(self.packet_body)

    def get_packet(self):
        return self.full_packet_data

import inspect
from aoko.enums.packet import AokoPacketFieldType,AokoPacketHooker
from aoko.codecs.encode import Encode
from aoko.entities.aoko_field import AokoField
from aoko.codecs.field_encode import _encode_field

class AokoPacketCrafter:
    def __init__(self,
                 auto_reset: bool =False,
                 enable_safe_check : bool = True,
                 debug: bool = False):


        self.reset = auto_reset
        self.enable_safe_check = enable_safe_check
        self.debug = debug
        self.fields = bytearray()
        self.full_packet_data = bytearray()

        self.un_packet_value: list[tuple[str]] = []

        self.packet_length = b''
        self.packet_id = None
        self.packet_body = bytearray()
        self.payload = bytearray()

        self.fields: list[bytes] = []

        #hooker
        self.before_build = []
        self.before_packet_id_encode = []
        self.after_packet_id_encode = []
        self.before_encode_field = []
        self.after_encode_field = []

        self.before_packet_length_encode = []
        self.after_packet_length_encode = []
        self.after_build = []

    def _call_func(self,func,*args,**kwargs):

        sig = inspect.signature(func)
        if len(sig.parameters) >= 1:
            func(*args,**kwargs)
        else:
            func()

    def _safe_check(self):
        if not self.enable_safe_check:
            return True
        if self.packet_id is None:
            raise Exception("Packet ID is required. Please use set_packet_id()")
        return True

    def clean(self):
        self.payload = bytearray()
        self.full_packet_data = bytearray()
        self.packet_body = bytearray()
        self.packet_length = 0

    def add_field(self,field:AokoField) -> None:
        self.un_packet_value.append((str(field.field_type.value),str(field.value)))
        self.fields.append(field)

    def add_fields(self,fields: list[AokoField]) -> None:
        for field in fields:
            self.un_packet_value.append((str(field.field_type.value),str(field.value)))
        self.fields.extend(fields)

    def add_raw_field(self,byte: bytes) -> None:
        self.un_packet_value.append((str(AokoPacketFieldType._AOKORAWBYTE.value),repr(byte)))
        self.fields.append(byte)

    def set_packet_id(self,id) -> None:
        self.packet_id = id

    def set_hooker(self, at: AokoPacketHooker, func):
        if not callable(func):
            raise TypeError("func must be callable")

        match at:
            case AokoPacketHooker.BEFORE_BUILD:
                self.before_build.append(func)
            case AokoPacketHooker.BEFORE_PACKET_ID_ENCODE:
                self.before_packet_id_encode.append(func)
            case AokoPacketHooker.AFTER_PACKET_ID_ENCODE:
                self.after_packet_id_encode.append(func)
            case AokoPacketHooker.BEFORE_ENCODE_FIELD:
                self.before_encode_field.append(func)
            case AokoPacketHooker.AFTER_ENCODE_FIELD:
                self.after_encode_field.append(func)
            case AokoPacketHooker.BEFORE_PACKET_LENGTH_ENCODE:
                self.before_packet_length_encode.append(func)
            case AokoPacketHooker.AFTER_PACKET_LENGTH_ENCODE:
                self.after_packet_length_encode.append(func)
            case AokoPacketHooker.AFTER_BUILD:
                self.after_build.append(func)

    def insert_byte(self,index,byte):
        if self.full_packet_data.__len__() == 0:
            raise Exception("need to build first")

    def build_no_packet_length(self,
                               clean_data_on_build: bool = True,
                               return_on_build_success: bool=False):
        if clean_data_on_build:
            self.clean()

        self._safe_check()

        # load hooker at before build

        for func in self.before_build:
            self._call_func(func, self)

        # field loop

        for field in self.fields:
            if isinstance(field,AokoField):

                # load hooker at before encode field

                for func in self.before_encode_field:
                    func(self,field)
                encode_field = _encode_field(field)
                self.payload.extend(encode_field)

                for func in self.after_encode_field:
                    func(self,field,encode_field)

            else:
                self.payload.extend(field)


        # encode pck id
        for func in self.before_packet_id_encode: # before
            func(self,self.payload,self.packet_id)

        self.packet_body.extend(Encode.EncodeVarInt(self.packet_id))

        for func in self.after_packet_id_encode: # after
            func(self,self.payload,self.packet_body)

        self.packet_body.extend(self.payload)

        self.full_packet_data.extend(self.packet_body)

        for func in self.after_build:
            func(self,self.full_packet_data)

        if return_on_build_success:
            return self.full_packet_data

    def build_normal(self):
        body = self.build_no_packet_length(return_on_build_success=True)
        self.full_packet_data = bytearray()
        self.packet_length = Encode.EncodeVarInt(len(body))
        self.full_packet_data.extend(self.packet_length)
        self.full_packet_data.extend(body)

        return self.full_packet_data

    def get_unpacked(self):
        return self.un_packet_value

    def get_packet_as_bytearray(self):
        return self.full_packet_data

    def get_packet_as_bytes(self):
        return bytes(self.full_packet_data)

import zlib

from mclium.api import Read,Encode,Decode

if __name__ == '__main__':
    data = [
        b'\x10\x00\xff\x05\tlocalhostc\xde\x02',
        b'\x19\x00\x07kenftr_\x93\x8aQ\x8a\xa1\x0eL\x02\xab\xc1\xb5q\x1c\xb1\x0f\xee',
        b'\x02\x00\x03\x19\x00\x02\x0fminecraft:brand\x06fabric\x0f\x00\x00\x05en_us\x0c\x00\x01\x7f\x01\x00\x01',
    ]
    parser = b'\x02\x00\x02\x0fminecraft:brand\x06fabric'
    offset = 0
    packet_length, offset = Read.read_varint(parser, offset)
    print(packet_length)
    packet_length,offset = Read.read_varint(parser, offset)
    packet_id,offset = Read.read_varint(parser, offset)
    print(packet_id)

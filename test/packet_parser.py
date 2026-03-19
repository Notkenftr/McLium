import zlib

from mclium.api import Read,Encode,Decode
if __name__ == '__main__':
    data = b'\n\x00\x04\x00\x00\x00\x00\x02{3\x1f'

    offset = 0

    packet_length,offset = Read.read_varint(data,offset)
    data_length,offset = Read.read_varint(data,offset)
    payload = data[offset:offset+packet_length]

    if data_length == 0:
        inner_offset = 0
        packet_id,offset = Read.read_varint(payload,inner_offset)
        packet_data = payload[inner_offset:]
        print(packet_data)
    else:
        inner_offset = 0
        decompressed_data = zlib.decompress(payload)
        packet_id,offset = Read.read_varint(decompressed_data,inner_offset)
        packet_data = decompressed_data[inner_offset:]
        print(packet_id)

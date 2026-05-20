#include <cstdint>
#include <vector>

#include "../include/packet_api.h"
#include "../include/encode.h"
void PacketApi::add_field(uint8_t field)
{
    fields.push_back(field);
}

vector<uint8_t>
PacketApi::build_uncompress_packet()
{
    vector<uint8_t> packet;
    vector<uint8_t> body;
    auto pid = Encode::varint(packet_id);

    body.insert(body.end(), pid.begin(), pid.end());
    body.insert(
        body.end(),
        fields.begin(),
        fields.end()
    );

    auto length = Encode::varint(body.size());

    packet.insert(
        packet.end(),
        length.begin(),
        length.end()
    );
    packet.insert(
        packet.end(),
        body.begin(),
        body.end());
    return packet;
}

vector<uint8_t> PacketApi::build_no_length()
{
    vector<uint8_t> packet;
    auto pid = Encode::varint(packet_id);

    packet.insert(packet.end(), pid.begin(), pid.end());
    packet.insert(
        packet.end(),
        fields.begin(),
        fields.end()
    );

    return packet;
}

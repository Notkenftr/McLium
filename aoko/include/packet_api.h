
#pragma once

#include <cstdint>
#include <vector>

#ifndef AOKO_PACKET_API_H
#define AOKO_PACKET_API_H

using namespace std;


class PacketApi {
private:
    uint8_t packet_id;
    vector<uint8_t> fields;
public:
    PacketApi(uint8_t packet_id)
    {
        this->packet_id = packet_id;
    }
    void add_field(uint8_t field);
    vector<uint8_t> build_no_length();
    vector<uint8_t> build_uncompress_packet();
};



#endif //AOKO_PACKET_API_H

//
// Created by kenftr on 5/20/26.
//

#include <cstdint>
#include <vector>

#include "../include/encode.h"

vector<uint8_t>
Encode::varint(int32_t value)
{
    vector<uint8_t> result;

    while (true)
    {
        uint8_t temp =
            value & 0x7F;

        value >>= 7;

        if (value != 0)
        {
            temp |= 0x80;
        }

        result.push_back(temp);

        if (value == 0)
        {
            break;
        }
    }

    return result;
}
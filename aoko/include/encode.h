//
// Created by kenftr on 5/20/26.
//

#ifndef AOKO_ENCODE_H
#define AOKO_ENCODE_H


#pragma once

#include <cstdint>
#include <vector>

using namespace std;

class Encode
{
public:
    static vector<uint8_t>
    varint(int32_t value);
};

#endif //AOKO_ENCODE_H

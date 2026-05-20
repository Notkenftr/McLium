#include <iostream>
#include <cstdint>
#include <vector>
#include "include/packet_api.h"
// TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.

int main()
{
    PacketApi p;
    p.add_field(255);
    auto data = p.build_uncompress_packet();

    for (auto b: data)
    {
        cout << int(b) << endl;
    }
}
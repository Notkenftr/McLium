#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "packet_api.h"
#include "encode.h"

namespace py = pybind11;

struct PyEncode {
    static std::vector<uint8_t> varint(uint32_t value) {
        return Encode::varint(value);
    }
};

PYBIND11_MODULE(aoko, m) {
    m.doc() = "Aoko Packet API bindings";

    py::class_<PyEncode>(m, "Encode")
        .def("varint", &PyEncode::varint);

    py::class_<PacketApi>(m, "PacketApi")
    .def(py::init<int>())
    .def("add_field", &PacketApi::add_field, "Add a field to the packet")
    .def("build_no_length", &PacketApi::build_no_length, "Build packet without length prefix")
    .def("build_uncompress_packet", &PacketApi::build_uncompress_packet);
    m.def("build_uncompress_packet", &PacketApi::build_uncompress_packet,
          "Build uncompressed packet");
}
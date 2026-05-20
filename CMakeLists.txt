cmake_minimum_required(VERSION 3.20)
project(Aoko LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

add_library(aoko_core STATIC
        src/packet_api.cpp
        codec/encode.cpp
)

target_include_directories(aoko_core PUBLIC include)


add_library(aoko MODULE bindings.cpp)

target_link_libraries(aoko PRIVATE
        aoko_core
        pybind11::module
        Python3::Python
)
target_include_directories(aoko PRIVATE include)

set_target_properties(aoko PROPERTIES
        PREFIX ""
        SUFFIX ".so"
)

add_executable(aoko_cli main.cpp)
target_link_libraries(aoko_cli PRIVATE aoko_core)
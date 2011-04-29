cmake_minimum_required(VERSION 2.8)
project(buildplmipmap)
if(COMMAND cmake_policy)
    cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

find_package(HSPlasma REQUIRED)
find_package(DevIL REQUIRED)

include_directories(${HSPlasma_INCLUDE_DIRS})
include_directories(${IL_INCLUDE_DIR})

add_executable(buildplmipmap buildplmipmap.cpp)
target_link_libraries(buildplmipmap HSPlasma ${IL_LIBRARIES} ${ILU_LIBRARIES})
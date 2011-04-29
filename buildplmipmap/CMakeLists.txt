cmake_minimum_required(VERSION 2.8)
project(buildplmipmap)
if(COMMAND cmake_policy)
    cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

find_package(HSPlasma REQUIRED)
find_package(DevIL REQUIRED)

include_directories(${HSPlasma_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/3rdPartyLibs/squish)
include_directories(${IL_INCLUDE_DIR})

set(SQUISH
    3rdPartyLibs/squish/alpha.cpp
    3rdPartyLibs/squish/alpha.h
    3rdPartyLibs/squish/clusterfit.cpp
    3rdPartyLibs/squish/clusterfit.h
    3rdPartyLibs/squish/colourblock.cpp
    3rdPartyLibs/squish/colourblock.h
    3rdPartyLibs/squish/colourfit.cpp
    3rdPartyLibs/squish/colourfit.h
    3rdPartyLibs/squish/colourset.cpp
    3rdPartyLibs/squish/colourset.h
    3rdPartyLibs/squish/maths.cpp
    3rdPartyLibs/squish/maths.h
    3rdPartyLibs/squish/rangefit.cpp
    3rdPartyLibs/squish/rangefit.h
    3rdPartyLibs/squish/singlecolourfit.cpp
    3rdPartyLibs/squish/singlecolourfit.h
    3rdPartyLibs/squish/squish.cpp
    3rdPartyLibs/squish/squish.h
)

add_executable(buildplmipmap buildplmipmap.cpp ${SQUISH})
target_link_libraries(buildplmipmap HSPlasma ${IL_LIBRARIES} ${ILU_LIBRARIES})
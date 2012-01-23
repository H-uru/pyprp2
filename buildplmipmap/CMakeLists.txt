cmake_minimum_required(VERSION 2.8)
project(buildplmipmap)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
set(PYTHON_3_OK TRUE)
set(PYTHON_2_OK FALSE)
if(COMMAND cmake_policy)
    cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

find_package(HSPlasma REQUIRED)
find_package(DevIL REQUIRED)
find_package(Python REQUIRED)

include_directories(${HSPlasma_INCLUDE_DIRS})
include_directories(${IL_INCLUDE_DIR})
include_directories(${PYTHON_INCLUDE_DIR})

add_library(buildplmipmap SHARED buildplmipmap.cpp)
target_link_libraries(buildplmipmap HSPlasma ${IL_LIBRARIES} ${ILU_LIBRARIES} ${PYTHON_LIBRARIES})
set_target_properties(buildplmipmap PROPERTIES
                      PREFIX ""
)
if(WIN32)
    set_target_properties(buildplmipmap PROPERTIES
                          SUFFIX ".pyd"
    )
endif()

EXECUTE_PROCESS(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; sys.stdout.write('.'.join([str(x) for x in sys.version_info[:2]]))"
                OUTPUT_VARIABLE _PYTHON_VERSION
)
EXECUTE_PROCESS(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; sys.stdout.write(sys.prefix)"
                OUTPUT_VARIABLE _PYTHON_PREFIX
)

if(NOT WIN32)
    install(TARGETS buildplmipmap
            DESTINATION ${_PYTHON_PREFIX}/lib/python${_PYTHON_VERSION}
    )
else()
    install(TARGETS buildplmipmap
            RUNTIME DESTINATION bin
            LIBRARY DESTINATION lib
            ARCHIVE DESTINATION lib
    )
endif()

cmake_minimum_required(VERSION 3.5)
project(pulp-tools VERSION 1.0.0)
include(ExternalProject)

option(WithFrameBuffer "Build with framebuffer support" OFF)
option(WithFTDI "Build with FTDI support" ON)
option(WithConfigGenerators "Install the config tools" ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "RelWithDebInfo"
        CACHE STRING "Choose the type of build, options are: Debug Release RelWithDebInfo MinSizeRel."
        FORCE
    )
endif(NOT CMAKE_BUILD_TYPE)

macro(add_project name)

    ExternalProject_Add(
        ${name}
        SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/${name}
        DOWNLOAD_COMMAND ""
        LOG_DOWNLOAD ON
        CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} -DCMAKE_IGNORE_PATH=${CMAKE_IGNORE_PATH} ${ARGN}
    )
endmacro()

add_project(json-tools)
add_project(pulp-configs -DWithConfigGenerators=${WithConfigGenerators})
add_project(pulp-debug-bridge -DWithFrameBuffer=${WithFrameBuffer} -DWithFTDI=${WithFTDI})

add_custom_target(pulp-tools ALL)

add_dependencies(pulp-configs json-tools)
add_dependencies(pulp-debug-bridge pulp-configs)
add_dependencies(pulp-tools pulp-debug-bridge)

install(CODE "")
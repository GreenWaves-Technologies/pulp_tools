cmake_minimum_required(VERSION 3.5)
project(pulp-tools VERSION 1.0.0)
include(ExternalProject)

option(WithFrameBuffer "Build with framebuffer support" OFF)
option(WithFTDI "Build with FTDI support" ON)
option(WithConfigGenerators "Install the config tools" ON)
option(WithPulpBridge "Install PULP bridge" OFF)
option(WithPulpSimulator "Install PULP GVSOC" ON)

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
        CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} -DCMAKE_IGNORE_PATH=${CMAKE_IGNORE_PATH} ${ARGN}
    )
endmacro()

macro(add_make_project name target)
    ExternalProject_Add(
        ${name}
        SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/${name}
        DOWNLOAD_COMMAND ""
        CONFIGURE_COMMAND ""
        BUILD_IN_SOURCE ON
        BUILD_ALWAYS ON
        BUILD_COMMAND PATH=$ENV{PATH}:${CMAKE_INSTALL_PREFIX}/bin PYTHONPATH=$ENV{PYTHONPATH}:${CMAKE_INSTALL_PREFIX}/python PULP_SDK_INSTALL=${CMAKE_INSTALL_PREFIX} PULP_SDK_HOME=${CMAKE_INSTALL_PREFIX}/.. PULP_SDK_WS_INSTALL=${CMAKE_INSTALL_PREFIX} INSTALL_DIR=${CMAKE_INSTALL_PREFIX} TARGET_INSTALL_DIR=${CMAKE_INSTALL_PREFIX} BUILD_DIR=${name}-prefix/src/${name}-build make ${target}
        INSTALL_COMMAND ""
    )
endmacro()

macro(add_copy_project name source_dir dest_dir)
    ExternalProject_Add(
        ${name}
        SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/${name}
        DOWNLOAD_COMMAND ""
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ""
        BUILD_ALWAYS ON
        INSTALL_COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_LIST_DIR}/${name}/${source_dir} ${CMAKE_INSTALL_PREFIX}/${dest_dir}
    )
endmacro()

add_custom_target(pulp-tools-top ALL)

if(WithPulpSimulator)
    SET(WithPulpBridge ON)
endif()

if(WithPulpSimulator OR WithPulpBridge)
    add_project(json-tools)
endif()

if (WithPulpBridge)
    add_project(pulp-configs -DWithConfigGenerators=${WithConfigGenerators})
    add_project(pulp-debug-bridge -DWithFrameBuffer=${WithFrameBuffer} -DWithFTDI=${WithFTDI})

    add_dependencies(pulp-configs json-tools)
    add_dependencies(pulp-debug-bridge pulp-configs)
    
    add_dependencies(pulp-tools-top pulp-debug-bridge)
endif()

if(WithPulpSimulator)
    add_make_project(pulp-tools all)
    add_copy_project(archi include include)
    add_make_project(dpi-models build)
    add_make_project(runner sdk.build)
    add_make_project(gvsoc build)

    add_dependencies(dpi-models json-tools)

    add_dependencies(gvsoc pulp-debug-bridge)
    add_dependencies(gvsoc json-tools)
    add_dependencies(gvsoc pulp-tools)
    add_dependencies(gvsoc archi)
    add_dependencies(gvsoc dpi-models)
    add_dependencies(gvsoc runner)

    add_dependencies(pulp-tools-top gvsoc)
endif()


install(CODE "")
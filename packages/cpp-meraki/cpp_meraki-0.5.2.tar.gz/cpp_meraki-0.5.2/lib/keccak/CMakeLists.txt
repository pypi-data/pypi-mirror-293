# meraki: C/C++ implementation of Meraki, the Telestai Proof of Work algorithm.
# Copyright 2019 Pawel Bylica.
# Licensed under the Apache License, Version 2.0.

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

add_library(
    keccak
    ${include_dir}/meraki/keccak.h
    ${include_dir}/meraki/keccak.hpp
    keccak.c
    keccakf800.c
    keccakf1600.c
)

target_include_directories(keccak PUBLIC $<BUILD_INTERFACE:${include_dir}>$<INSTALL_INTERFACE:include>)

install(
    TARGETS keccak
    EXPORT merakiTargets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

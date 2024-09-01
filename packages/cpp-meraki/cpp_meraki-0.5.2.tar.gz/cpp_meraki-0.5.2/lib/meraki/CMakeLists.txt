# meraki: C/C++ implementation of Meraki, the Telestai Proof of Work algorithm.
# Copyright 2018-2019 Pawel Bylica.
# Licensed under the Apache License, Version 2.0.

include(GNUInstallDirs)

add_library(
    meraki
    bit_manipulation.h
    builtins.h
    endianness.hpp
    ${include_dir}/meraki/meraki.h
    ${include_dir}/meraki/meraki.hpp
    meraki-internal.hpp
    meraki.cpp
    ${include_dir}/meraki/hash_types.h
    managed.cpp
    kiss99.hpp
    primes.h
    primes.c
    ${include_dir}/meraki/progpow.hpp
    progpow.cpp
)

target_link_libraries(meraki PRIVATE keccak)
target_include_directories(meraki PUBLIC $<BUILD_INTERFACE:${include_dir}>$<INSTALL_INTERFACE:include>)
if(CABLE_COMPILER_GNULIKE AND NOT SANITIZE MATCHES undefined)
    target_compile_options(meraki PRIVATE $<$<COMPILE_LANGUAGE:CXX>:-fno-rtti>)
endif()

install(
    TARGETS meraki
    EXPORT merakiTargets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

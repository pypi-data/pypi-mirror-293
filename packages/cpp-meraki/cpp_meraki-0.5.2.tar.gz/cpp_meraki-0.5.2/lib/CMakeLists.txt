# meraki: C/C++ implementation of Meraki, the Telestai Proof of Work algorithm.
# Copyright 2019 Pawel Bylica.
# Licensed under the Apache License, Version 2.0.

add_subdirectory(keccak)
add_subdirectory(meraki)

get_filename_component(MERAKI_PRIVATE_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR} ABSOLUTE)
set(MERAKI_PRIVATE_INCLUDE_DIR ${MERAKI_PRIVATE_INCLUDE_DIR} PARENT_SCOPE)

# meraki: C/C++ implementation of Meraki, the Telestai Proof of Work algorithm.
# Copyright 2019 Pawel Bylica.
# Licensed under the Apache License, Version 2.0.

# The CFFI build script for meraki library.
# It expects the library is installed in the dist/ directory.
# The installation can be performed by
#
#     cmake . -DCMAKE_INSTALL_PREFIX=dist
#     make
#     make install

from cffi import FFI
import sys

ffibuilder = FFI()

stdlib = []
if sys.platform == 'linux':
    stdlib.append('stdc++')

ffibuilder.set_source(
    "_meraki",
    r"""
    #include <meraki/keccak.h>
    #include <meraki/meraki.h>
     """,
    include_dirs=['include'],
    libraries=['meraki', 'keccak'] + stdlib,
)

ffibuilder.cdef("""

union meraki_hash256
{
    ...;
    char str[32];
};

union meraki_hash512
{
    ...;
    char str[64];
};

struct meraki_result
{
    union meraki_hash256 final_hash;
    union meraki_hash256 mix_hash;
};


union meraki_hash256 meraki_keccak256(const uint8_t* data, size_t size);

union meraki_hash512 meraki_keccak512(const uint8_t* data, size_t size);

const struct meraki_epoch_context* meraki_get_global_epoch_context(int epoch_number);

struct meraki_result meraki_hash(const struct meraki_epoch_context* context,
    const union meraki_hash256* header_hash, uint64_t nonce);
    
bool meraki_verify(const struct meraki_epoch_context* context,
    const union meraki_hash256* header_hash, const union meraki_hash256* mix_hash, uint64_t nonce,
    const union meraki_hash256* boundary);

union meraki_hash256 light_verify(const union meraki_hash256* header_hash, const union meraki_hash256* mix_hash, uint64_t nonce);                            

""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

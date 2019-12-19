#!/usr/bin/env python3
import os, sys

sdk_path = ''
if len(sys.argv) > 1:
    sdk_path = sys.argv[1] 

if not os.path.exists(sdk_path):
    sdk_path = '/opt/intel/sgxsdk/include'

header_filename = os.path.join(sdk_path, 'sgx_error.h')

if not os.path.exists(header_filename):
    print('UNABLE TO FIND HEADER FILE sgx_error.h. Provide path to sgx sdk.')
    print('Looked for sdk here: ' + sdk_path)
    print('Looked for file here: ' + header_filename)
    exit(1)

print('// This is an autogenerated file based on the Intel SGX SDK file: sgx_error.h')
print('// It "handles" an error by printing and returning false.')
print('// In some cases the application could retry after these failures.')
print('#include <iostream>')
print('#include "sgx_error.h"')
print('using namespace std;')
print()
print('bool HandleSgxErr(sgx_status_t ret){')
print('    if (ret == SGX_SUCCESS) { cout << "SUCCESS\\n"; return(1);}')
print('    cerr << hex;')
print('    switch(ret){')

with open(header_filename) as f:
    for line in f:
        if not " SGX_ERROR" in line:
            continue
        code = line.split('=')[0].strip()
        msg = line.split('/*')[1].strip()[:-3]
        print('    case ' + code +':')
        print('        cerr << "' + code + ': ";')
        print('        cerr << "' + msg + '\\n";')
        print('        break;')

print('    default:')
print('        cerr << "UNKNOWN SGX ERROR:" << ret << "\\n";')
print('    }')
print('    cerr << dec;')
print('return(false);')
print('}')
f.close()

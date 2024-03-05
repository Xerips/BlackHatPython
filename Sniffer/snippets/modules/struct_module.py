import ipaddress
import struct

class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff) # First character < or > determins endianness.
        self.ver = header[0] >> 4 # Right shift 4 places (prepend 4 0's) to get a high order 4 bit nibble.
        self.ihl = header[0] & 0xF # Sets the first 4 bits to False 0 AND retains the last 4 bits as True.

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # Human readable IP addresses.
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # Map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

class ICMP:
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

'''
instantiate with:

mypacket = IP(buff)
print(f'{mypacket.src_address} -> {mypacket.dst_address}')
'''

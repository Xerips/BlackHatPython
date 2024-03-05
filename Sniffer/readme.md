# Sniffer

This chapter of the book is very inconsistent with indenting and has multiple issues with the code. I did some trouble shooting and scanner.py works, you just need to edit the SUBNET at the top of the tool to match your target.  
I've included in this section a directory full of the snippets from the book that lead up to sniffer.py.  

### scanner.py

Edit SUBNET in the tool to SUBNET = '<Target Subnet>' and let her run!  
This tool will print out the IP addresses of all active hosts it can find on a given subnet.  
Why/When: If you've gotten a foothold on a target and want to enumerate the subnet it's on, you can run this tool while on your target to do so.  

# Snippets

### UDP Host Discovery Tools

These tools work by spraying a network with UDP datagrams to (hopefully) closed ports. We know there is a host active when we receive a "port unreachable" ICMP message because "something" sent us the ICMP message.  
The tools here are a great starting point to implement additional logic to work with the host discovery. Think kicking off an nmap scan of all discovered hosts automatically.  

### basic_HostDiscovery.py

Basic script to sniff a packet and determine whether the host is Windows or not. We need to know whether a host is running Windows because if so we need to change the way we interact with it - No promiscuous mode, be aware of (IOCTL)[http://en.wikipedia.org/wiki/Ioctl].  
Windows lets us sniff all incoming packets, Linux forces us to specify that we are sniffing ICMP packets.  
This tool requires elevated privileges to run.  
Learn about (IP Protocol Headers)[https://www.thegeekstuff.com/2012/03/ip-protocol-header/] to help understand how to decode incoming packets.  

### sniffer_ip_header_decode.py

Combines basic_HostDiscovery.py and s_decode_module.py (not instantiated but written), to create an IP header sniffer that decodes the packets.  
I found that I kept getting the error "sniff" not defined when using the code from the book, so I changed it up a bit to work.  
Book code is sniffer_ip_header_decode.book.py, the edited code is sniffer_ip_header_decode.py  

# Modules

The book doesn't do this, but in reality if you've created these modules, instead of copy+pasting/typing them out in your code every time, you would just import the module and use it that way. Allowing you to make changes to the modules without making changes to your main code.  

#### ctypes_module: (ctypes Documentation)[https://docs.python.org/3/library/ctypes.html]

You can use either ctypes or struct module for decoding incoming packets. They do essentially the same thing.  
ctypes: A foreign library that bridges to C-based languages to use C-compatible data types and call functions in shared libraries. Handles binary data types in addition to providing a lot of other functionality.  
Notice each field matches an IP-Protocol Header field.  
Each field takes 3 arguments: the name of the field, the type of value it takes, and the bit width.  

#### struct_module: (struct Documentation)[https://docs.python.org/3/library/struct.html]

You can use either ctypes or struct module for decoding incoming packets. They do essentially the same thing.  
struct: primarily handles binary data.  
Module requires you to know the endianness of your system. Kali and Arch are little-endian and so is this tool. I use arch, btw.  
    You can find more information on big/little-endian in the struct docs linked above.  
Breaking down ```struct.unpack('<BBHHHBBH4s4s>', buff)```  
    B = 1-byte unsigned char)  
    H = 2-byte unsigned short)  
    s = a byte array that requires a byte-width specification, 4s means 4-byte string.  
In ctypes we specified bit-width of header parts, but with struct there is no format character for 4-bit units of data (half a byte is a nibble - cuz nerds are fun). See the code for commends on binary manipulation with .ver and .ihl to access high-order and low-order half bytes.  

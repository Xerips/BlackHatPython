import socket

target_host = "127.0.0.1"
target_port = 9997

# create a socket object
# IF_INET indicates we are using IPv4 for the host name
# SOCK_DGRAM sets the client to UDP, There is no call to connect() because UDP is connectionless
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
client.sendto(b"AAABBBCCC",(target_host,target_port))

# receive some data
#revfrom() is used to receive UDP data from the server
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()

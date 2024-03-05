import socket

target_host = "127.0.0.1"
target_port = 9998

# create a socket object
# AF_INET parameter indicates we'll use IPv4 address or hostname
# SOCK_STREAM indicates this will be a TCP client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))

# send some data
# the (b"<data>") formatting sends the GET request as bytes
client.send(b"GET / HTTP/1.1\r\nHost: It's ME!\r\n\r\n")

# recieve some data
response = client.recv(4096)

print(response.decode())
client.close()

'''
This script assumes the connect will be always be made, and that the server expects us to send data first. Some servers will send data first and wait a response.
'''

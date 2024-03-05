import socket
import threading

IP = "0.0.0.0"
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT)) # Pass IP and Port #'s to the server to start listening on.
    server.listen(5) # Tell the server to start listening with a maximum of 5 backlogged connections.
    print(f'[*] Listening on {IP}:{PORT}') 

    # 1. When a client connects, we receive the client socket in the client variable and the remote connection variables in the address variable.
    # 2. Create a new thread object that points to handle_client function and pass it the client socket object as an argument.
    # 3. Start the thread to handle client connection. The loop then starts over listening for additional clients.
    while True:
        client, address = server.accept() # 1.
        print(f'[*] Accept connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,)) # 2.
        client_handler.start() # 3.

# performs the recv() function and sends a simple message back to the client.
def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == '__main__':
    main()

'''
This script and TCPclient.py are setup to work together, you can start this script, then run the TCPclient.
This will test that both are working and show the output for each.
'''

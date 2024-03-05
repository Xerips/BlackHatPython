import argparse
import socket
import shlex
import subprocess # Process-creation interface that interacts with client programs. Used for check_output.
import sys
import textwrap
import threading

# Execute function receives a command, runs it, and returns the output as a string.
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

# The plumbing:
class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self): # The send method
        self.socket.connect((self.args.target, self.args.port)) # Connect and send buffer if buffer.
        if self.buffer:
            self.socket.send(self.buffer)

        try: # Setup try/catch block so we can manually close connection with Ctrl+c.
            while True: # Start loop to receive data from target, if no more data, break out of loop.
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break # Break out of loop if no more data.
                if response: # Print the response data and pause to get interactive input and continue the loop.
                    print(response)
                    buffer = input ('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt: # Loop continues until you close the script with Ctrt+c.
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self): # The listen method.
        self.socket.bind((self.args.target, self.args.port)) # Listen method binds to the target port.
        self.socket.listen(5)
        while True: # Starts the listening Loop.
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread( # Passes the connected socket to the handle method.
                target=self.handle, args=(client_socket,))
            client_thread.start()

    def handle(self, client_socket): # File upload logic.
        if self.args.execute: # If a command should be executed, pass command to execute function and send back output.
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        elif self.args.upload: # Set up a loop to listen for data and recieve data until none is left.
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data 
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        elif self.args.command: # If a shell is to be created, send a prompt to the sender & wait for a command string.
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'NC: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'Server Killed {e}')
                    self.socket.close()
                    sys.exit()

# Setting up args parser and script info in __main__.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t $IP -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t $IP -p 5555 -l -e \"cat /etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t $IP -p 135 # echo text to server port 135
            netcat.py - t $IP -p 5555 -p 5555 # connect to server
        '''))
parser.add_argument('-c', '--command', action='store_true', help='command shell')
parser.add_argument('-e', '--execute', help='execute specified command')
parser.add_argument('-l', '--listen', action='store_true', help='listen')
parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
parser.add_argument('-t', '--target', default='$IP', help='specified IP') # I often set a target variable for $IP.
parser.add_argument('-u', '--upload', help='upload file')
args = parser.parse_args()
if args.listen:
    buffer = ''
else:
    buffer = sys.stdin.read()

nc = NetCat(args, buffer.encode())
nc.run()


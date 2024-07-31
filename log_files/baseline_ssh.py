import paramiko
import socket
import threading
import time

# Define a simple server interface
class SimpleSSHServer(paramiko.ServerInterface):
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'user' and password == 'pass':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        return True

# Function to handle the SSH session
def handle_client(client_socket):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(host_key)
    server = SimpleSSHServer()

    try:
        transport.start_server(server=server)
        chan = transport.accept(20)
        if chan is None:
            print("No channel")
            return
        standard = "Welcome to the simple SSH server!\n"
        multi = standard * 2
        for char in multi:
            chan.send(char)
            time.sleep(0.5)
        #chan.send("Welcome to the simple SSH server!\n")
        while True:
            command = chan.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                chan.send("Goodbye!\n")
                break
            chan.send(f"Received: {command}\n")
        chan.close()
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        transport.close()

# Function to start the SSH server
def start_server(host='0.0.0.0', port=2223):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(100)

    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    # Generate an RSA key for the SSH server
    host_key = paramiko.RSAKey(filename="server.key")
    start_server(port=2222)  # Use a non-privileged port for testing

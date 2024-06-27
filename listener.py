import socket

def server_program():
    host = socket.gethostname()
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for a single connection

    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connected to {addr[0]}:{addr[1]}")

    while True:
        command = input("Enter a command to send to the client: ")
        conn.send(command.encode("utf-8"))

        response = conn.recv(1024).decode("utf-8")
        print(f"Client response: {response}")

    conn.close()

if __name__ == "__main__":
    server_program()

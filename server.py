import socket
import threading
import sys

class ListenerThread(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_socket.bind(('localhost', self.port))
        self.listener_socket.listen()
        self.thread_id = self.ident

    def run(self):

        print(f"Listener {self.thread_id} started on port {self.port}")
        while True:
            connection, address = self.listener_socket.accept()
            print(f"Connection established with {address}")
            data = connection.recv(64)
            if len(data) > 0:
                print(f"Received data: {data.decode('utf-8')}")
                # Add your custom logic here based on the received data
                # For example, process commands or respond to the client
            connection.close()

def main():
    counter = 0
    listeners = {}  # Dictionary to store listener threads
    x = True
    while x:
        user_input = input("Enter 'start <port>', 'kill <id>', or 'list': ")
        parts = user_input.split()
        if len(parts) == 2:
            command, arg = parts
            if command.lower() == "start":
                try:
                    port = int(arg)
                    listener = ListenerThread(port)
                    listener.start()
                    listeners[counter] = listener
                    print(f"Listener {counter} started on port {port}")
                    counter += 1
                except ValueError:
                    print("Invalid port. Please enter a valid integer.")
            elif command.lower() == "kill":
                try:
                    thread_id = int(arg)
                    listener = listeners.get(thread_id)
                    if listener:
                        listener.listener_socket.close()
                        listener.join()
                        del listeners[thread_id]
                        print(f"Listener {thread_id} killed.")
                    else:
                        print(f"No listener with ID {thread_id} found.")
                except ValueError:
                    print("Invalid ID. Please enter a valid integer.")
            else:
                print("Invalid command. Please enter 'start <port>', 'kill <id>', or 'list'.")
        elif user_input.lower() == "list":
            print("Active listeners:")
            for listener in listeners.values():
                print(threading. enumerate() )
        elif user_input.lower() == "exit":
            x = False
        else:
            print("Invalid input. Please follow the format: 'start <port>', 'kill <id>', or 'list'.")

if __name__ == "__main__":
    main()

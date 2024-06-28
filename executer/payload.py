import socket
import subprocess

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True)
        return result.decode("utf-8")
    except subprocess.CalledProcessError:
        return "Error executing command"
    
def client_program():
    host = socket.gethostname()
    port = 12345

    client_socket = socket.socket()
    client_socket.connect((host, port))

    while True:
        command = client_socket.recv(1024).decode("utf-8")
        print(f"Received command from server: {command}")

        # Process the command (you can modify this part)
        result = execute_command(command)
        response = f"Command '{command}' executed successfully"
        client_socket.send(response.encode("utf-8"))

if __name__ == "__main__":
    client_program()

import socket

# Server configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 1234         # Server's port

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    connected = True
    while connected:
        msg = input("Enter message to send (or 'exit' to quit): ")
        if msg.lower() == 'exit':
            connected = False
            client.close()
        else:
            client.send(msg.encode("utf-8"))
            response = client.recv(1024).decode("utf-8")
            print(f"[SERVER] {response}")

if __name__ == "__main__":
    start_client()

import socket
import threading

class Client:
    def __init__(self, ip):
        self.ip = ip


class Server:
    def __init__(self, host="127.0.0.1", port=1234):
        self.clients = []
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"[STARTING] Server started on {self.host}:{self.port}")


Server()

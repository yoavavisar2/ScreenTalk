from tkinter import *
from client import Client
import socket
import threading


def pixels2points(pixels):
    return int(0.75 * pixels)


class StreamPage(Frame):
    def __init__(self, root, width, height, client: Client, ip):
        super().__init__(root, bg="#031E49")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height
        self.other_user = ip
        self.connected = True

        if self.other_user == '127.0.0.1':
            self.ip = '127.0.0.1'
        else:
            hostname = socket.gethostname()
            self.ip = socket.gethostbyname(hostname)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (self.ip, 12345)
        self.socket.bind(self.address)

        threading.Thread(target=self.receive).start()

    def receive(self):
        while self.connected:
            msg = self.socket.recv(1024).decode()
            print(msg)


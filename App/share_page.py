from tkinter import *
from client import Client
import socket
import threading


def pixels2points(pixels):
    return int(0.75 * pixels)


class SharePage(Frame):
    def __init__(self, root, width, height, client: Client, ip):
        super().__init__(root, bg="#031E49")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height
        self.other_user = ip
        self.connected = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((self.other_user, 12345))

        threading.Thread(target=self.send_msg).start()

    def send_msg(self):
        while self.connected:
            print("enter:")
            msg = input()
            self.socket.send(msg.encode())

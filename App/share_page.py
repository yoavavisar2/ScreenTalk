from tkinter import *
from client import Client


def pixels2points(pixels):
    return int(0.75 * pixels)


class SharePage(Frame):
    def __init__(self, root, width, height, client: Client, ip):
        print(123)
        super().__init__(root, bg="#031E49")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height
        self.other_user = ip

        print(self.other_user)

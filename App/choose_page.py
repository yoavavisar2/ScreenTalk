from tkinter import *
from client import Client


def pixels2points(pixels):
    return int(0.75 * pixels)


class ChoosePage(Frame):
    def __init__(self, root, width, height, client: Client):
        super().__init__(root, bg="#031E49")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height

        Label(self, text=f"welcome {self.client.username}", font=("ariel", pixels2points(self.width/20)),
              bg="#031E49", fg="white").pack(pady=self.height // 20)

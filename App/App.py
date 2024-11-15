import socket
from home_page import HomePage
from tkinter import *
import threading
from threading import Event
import sys

class App:
    def __init__(self, host='127.0.0.1', port=1234):
        self.host = host
        self.port = port

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        self.root = Tk()
        HomePage(self.root, self.client)
        self.root.mainloop()

        self.client.close()
        sys.exit()


if __name__ == '__main__':
    App()

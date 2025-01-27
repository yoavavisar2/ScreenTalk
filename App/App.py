from home_page import HomePage
from tkinter import *
import sys
from client import Client


class App:
    def __init__(self):
        self.client = Client('192.168.24.209')

        self.root = Tk()
        HomePage(self.root, self.client)
        self.root.mainloop()

        self.client.client.send(self.client.encrypt("exit:"))
        self.client.client.close()
        sys.exit()


if __name__ == '__main__':
    App()

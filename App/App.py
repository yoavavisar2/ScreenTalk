import socket
from home_page import HomePage
from tkinter import *
import threading
import sys

class App:
    def __init__(self, host='127.0.0.1', port=1234):
        self.host = host
        self.port = port

        self.client = None
        self.root = None

        threading.Thread(target=self.start_client, daemon=True).start()

        threading.Thread(target=self.start_gui).start()

    def start_gui(self):
        self.root = Tk()
        HomePage(self.root)
        self.root.mainloop()
        self.client.close()
        sys.exit()

    def start_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        connected = True
        while connected:
                msg = input("Enter message to send (or 'exit' to quit): ")
                if msg.lower() == 'exit':
                    connected = False
                    self.client.close()
                else:
                    self.client.send(msg.encode("utf-8"))
                    response = self.client.recv(1024).decode("utf-8")
                    print(f"[SERVER] {response}")


if __name__ == '__main__':
    App()

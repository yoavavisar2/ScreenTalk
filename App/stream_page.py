from tkinter import *
from client import Client
import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from io import BytesIO
from PIL import Image, ImageTk
from pynput import keyboard
from pynput import mouse


class StreamPage(Frame):
    def __init__(self, root, width, height, client: Client, ip, key):
        super().__init__(root, bg="#031E49")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height
        self.other_user = ip
        self.connected = True
        self.key = key

        self.x = 0
        self.y = 0

        self.events = []

        if self.other_user == '127.0.0.1':
            self.ip = '127.0.0.1'
        else:
            hostname = socket.gethostname()
            self.ip = socket.gethostbyname(hostname)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (self.ip, 12345)
        self.socket.bind(self.address)

        threading.Thread(target=self.stream).start()
        threading.Thread(target=self.send_keyboard).start()
        threading.Thread(target=self.send_mouse).start()

    def get_mouse_position(self, event):
        width = self.width * 0.75
        height = self.height * 0.75

        self.x, self.y = event.x / width, event.y / height

    def on_click(self, x, y, button, pressed):
        event = f"click:{button}"
        self.events.append(event)

    def on_scroll(self, x, y, dx, dy):
        event = f"scroll:{dx},{dy}\n"
        self.events.append(event)

    def send_mouse(self):
        listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll)
        listener.start()
        while self.connected:
            try:
                data = "move:" + str(self.x) + "/" + str(self.y)
                data = self.encrypt_aes(data.encode())
                self.socket.sendto(data, (self.other_user, 12347))
                while self.events:
                    event = self.events.pop(0)
                    event = self.encrypt_aes(event.encode())
                    self.socket.sendto(event, (self.other_user, 12347))
            except socket.error:
                self.connected = False

    def send_keyboard(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            while self.connected:
                if not self.connected:
                    listener.stop()
                    break
                listener.join(1)

    def on_press(self, key_pressed):
        try:
            key = str(key_pressed.char)
        except AttributeError:
            key = str(key_pressed)
        data = "keyboard:" + key
        data = self.encrypt_aes(data.encode())
        self.socket.sendto(data, (self.other_user, 12346))

    def stream(self):
        canvas = Canvas(self, width=self.width * 0.75, height=self.height * 0.75)
        canvas.pack()
        canvas.bind("<Motion>", self.get_mouse_position)
        while True:
            try:
                # Receive image data over UDP
                data, addr = self.socket.recvfrom(1024 * 1024)
                data = self.decrypt_aes(data)

                # Convert bytes to image
                image = Image.open(BytesIO(data))
                image = image.resize((int(self.width * 0.75), int(self.height * 0.75)))
                photo = ImageTk.PhotoImage(image)

                # Display image on canvas
                canvas.create_image(0, 0, anchor=NW, image=photo)
                canvas.image = photo  # Prevent garbage collection
            except Exception as e:
                print(f"Error receiving or displaying screen: {e}")

    def encrypt_aes(self, plaintext: bytes):
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()

        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        return iv + ciphertext

    def decrypt_aes(self, encrypted_data) -> bytes:
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext

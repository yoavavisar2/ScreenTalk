from tkinter import *
from client import Client
import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from PIL import ImageGrab
from io import BytesIO
from pynput.keyboard import Controller as keyboardController
from pynput.mouse import Button, Controller as mouseController
from keys import key_mapping


class SharePage(Frame):
    def __init__(self, root, width, height, client: Client, ip, key):
        super().__init__(root, bg="#000000")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height
        self.other_user = ip
        self.connected = True
        self.key = key

        if self.other_user == '127.0.0.1':
            self.ip = '127.0.0.1'
        else:
            hostname = socket.gethostname()
            self.ip = socket.gethostbyname(hostname)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (self.ip, 12346)
        self.socket.bind(self.address)

        threading.Thread(target=self.share).start()
        threading.Thread(target=self.receive_keyboard_mouse).start()

    def receive_keyboard_mouse(self):
        keyboard = keyboardController()
        mouse = mouseController()
        while self.connected:
            data, addr = self.socket.recvfrom(1024 * 1024)
            data = self.decrypt_aes(data).decode()
            header, data = data.split(":")
            if header == "keyboard":
                try:
                    keyboard.press(data)
                except:
                    keyboard.press(key_mapping[data])
            if header == "move":
                x, y = data.split('/')
                x = float(x) * self.width
                y = float(y) * self.height

                mouse.position = (x, y)

    def share(self):
        try:
            while True:
                # Capture the screen
                screenshot = ImageGrab.grab()

                # Resize for better performance (optional)
                screenshot = screenshot.resize((1000, 750))

                # Convert image to bytes
                bio = BytesIO()
                screenshot.save(bio, format="JPEG", quality=75)
                image_bytes = bio.getvalue()

                # Send image data over UDP
                self.socket.sendto(self.encrypt_aes(image_bytes), (self.other_user, 12345))
        except Exception as e:
            print(f"Error capturing or sending screen: {e}")

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

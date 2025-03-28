from tkinter import *
from client import Client
import socket as s
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from PIL import ImageGrab
from io import BytesIO
from pynput.keyboard import Controller as keyboardController
from pynput.mouse import Button as mouseButton, Controller as mouseController
from keys import key_mapping


class SharePage(Frame):
    def __init__(self, root, width, height, client: Client, ip, key, back):
        super().__init__(root, bg="#000000")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height
        self.other_user = ip
        self.connected = True
        self.key = key
        self.back = back

        self.mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mouse_socket.bind((self.other_user, 12347))
        self.mouse_socket.listen(1)
        self.conn, _ = self.mouse_socket.accept()

        threading.Thread(target=self.receive_mouse).start()

    def receive_mouse(self):
        mouse = mouse.Controller()
        while self.connected:
            data = self.conn.recv(1024)
            if not data:
                break
            data = self.decrypt_aes(data).decode()
            header, data = data.split(":")
            if header == "move":
                x, y = data.split('/')
                x = float(x) * self.width
                y = float(y) * self.height
                mouse.position = (x, y)
            elif header == "click":
                button = mouse.Button.left if data == 'Button.left' else mouse.Button.right
                mouse.press(button)
                mouse.release(button)
            elif header == "scroll":
                dx, dy = map(int, data.split(','))
                mouse.scroll(dx, dy)

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

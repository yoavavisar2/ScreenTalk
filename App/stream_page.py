from tkinter import *
from client import Client
import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


def pixels2points(pixels):
    return int(0.75 * pixels)


class StreamPage(Frame):
    def __init__(self, root, width, height, client: Client, ip, key):
        super().__init__(root, bg="#031E49")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height
        self.other_user = ip
        self.connected = True
        self.key = key  # TODO: enc and dec funcs

        if self.other_user == '127.0.0.1':
            self.ip = '127.0.0.1'
        else:
            hostname = socket.gethostname()
            self.ip = socket.gethostbyname(hostname)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (self.ip, 12345)
        self.socket.bind(self.address)

        threading.Thread(target=self.receive).start()

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

    def receive(self):
        img_bytes = self.socket.recv(65535)
        img_bytes = self.decrypt_aes(img_bytes)

        with open("received_image.png", "wb") as file:
            file.write(img_bytes)

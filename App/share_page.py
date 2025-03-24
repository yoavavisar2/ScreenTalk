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

        if self.other_user == '127.0.0.1':
            self.ip = '127.0.0.1'
        else:
            hostname = s.gethostname()
            self.ip = s.gethostbyname(hostname)

        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.address = (self.ip, 12346)
        self.socket.bind(self.address)

        threading.Thread(target=self.share).start()
        threading.Thread(target=self.receive_keyboard).start()
        threading.Thread(target=self.receive_mouse).start()

    def mouse_events(self, mouse):
        host = s.gethostbyname(s.gethostname())
        port = 9999

        server = s.socket(s.AF_INET, s.SOCK_STREAM)
        server.bind((host, port))
        server.listen()

        c, addr = server.accept()

        while self.connected:
            event = c.recv(1024)
            event = self.client.decrypt(event).decode()

            header, data = event.split(':')
            if header == "click":
                button = data
                btn = mouseButton.left if button == 'Button.left' else mouseButton.right
                mouse.press(btn)
                mouse.release(btn)
            if header == "scroll":
                dx, dy = data.split(',')
                mouse.scroll(int(dx), int(dy))

    def receive_mouse(self):
        socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        address = (self.ip, 12347)
        socket.bind(address)

        mouse = mouseController()

        threading.Thread(target=self.mouse_events, args=(mouse,)).start()

        while self.connected:
            data, addr = socket.recvfrom(1024 * 1024)
            data = self.decrypt_aes(data).decode()
            header, data = data.split(":")
            if header == "move":
                x, y = data.split('/')
                x = float(x) * self.width
                y = float(y) * self.height
                mouse.position = (x, y)
    # TODO: receive mouse events in tcp

    def receive_keyboard(self):
        keyboard = keyboardController()
        while self.connected:
            data, addr = self.socket.recvfrom(1024 * 1024)
            data = self.decrypt_aes(data).decode()
            header, data = data.split(":")
            if header == "keyboard":
                try:
                    keyboard.press(data)
                except:
                    keyboard.press(key_mapping[data])
                    keyboard.release(key_mapping[data])
            elif header == "exit":
                self.client.client.send(self.client.encrypt("ExitAllow:"))
                for widget in self.winfo_children():
                    widget.destroy()
                self.connected = False
                self.socket.close()
                self.destroy()

                self.back()
                # TODO: exit

    def send_image(self, image_bytes):
        chunk_size = 4096
        for i in range(0, len(image_bytes), chunk_size):
            chunk = image_bytes[i:i + chunk_size]
            self.socket.sendto(self.encrypt_aes(chunk), (self.other_user, 12345))
        self.socket.sendto(self.encrypt_aes(b"end"), (self.other_user, 12345))

    def share(self):
        while self.connected:
            try:
                # Capture the screen
                screenshot = ImageGrab.grab()

                # Resize for better performance (optional)
                screenshot = screenshot.resize((1440, 810))

                # Convert image to bytes
                bio = BytesIO()
                screenshot.save(bio, format="JPEG", quality=75)
                image_bytes = bio.getvalue()

                self.send_image(image_bytes)
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

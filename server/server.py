import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import sqlite3


def make_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

class Client:
    def __init__(self, addr, conn):
        self.addr = addr
        self.conn = conn
        self.private_key, self.public_key = make_keys()
        self.public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.connection = sqlite3.connect("aquarium.db")
        self.cursor = self.connection.cursor()

    def decrypt(self, encrypted_text):
        decrypted_message = self.private_key.decrypt(
            encrypted_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message

class Server:
    def __init__(self, host="127.0.0.1", port=1234):
        self.clients = []
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print("[STARTING]")
        self.start()

    def handle_client(self, client: Client):
        print("[NEW CONNECTION]")
        self.clients.append(client)

        client.conn.send(client.public_key_pem)

        connected = True
        while connected:
            try:
                msg = client.conn.recv(1024)
                msg = client.decrypt(msg).decode()
                header, data = msg.split(":")
                if header == "signup":
                    self.handel_signup(data)
                elif header == "login":
                    self.handel_login(data)
            except:
                connected = False

        print(f"[DISCONNECT]")
        try:
            self.clients.remove(client.conn)
            client.conn.close()
        except:
            pass

    def handel_signup(self, data):
        # check if user exists and add to sql
        pass

    def handel_login(self, data):
        # log the user
        print(data)

    def start(self):
        print("[LISTENING]")
        while True:
            conn, addr = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(Client(addr, conn),))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == '__main__':
    Server()

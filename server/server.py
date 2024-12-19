import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import sqlite3
from hashlib import sha256
import os

pepper = "yoav123"


def hashing(text, salt):
    global pepper
    data = salt + text.encode() + pepper.encode()
    for _ in range(10):
        data = sha256(data).digest()
    return data


def make_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


class Client:
    def __init__(self, addr, conn):
        self.addr = addr
        self.conn = conn
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        self.private_key, self.public_key = make_keys()
        self.public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

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


def is_user_exist(username, cursor: sqlite3.Cursor):
    cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    return cursor.fetchone() is not None


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
                    self.handel_signup(data, client.conn)
                elif header == "login":
                    self.handel_login(data, client.conn)
            except Exception as e:
                print(e)
                connected = False

        print(f"[DISCONNECT]")
        try:
            self.clients.remove(client.conn)
            client.conn.close()
        except:
            pass

    @staticmethod
    def handel_signup(data, client_conn: socket):
        values = data.split('/')
        first_name, second_name, username, password = values

        salt = os.urandom(16)

        password = hashing(password, salt)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        if not is_user_exist(username, cursor):
            cursor.execute("""
            INSERT INTO users (FirstName, LastName, Username, Password, salt) VALUES (?, ?, ?, ?, ?)
            """, (first_name, second_name, username, password, salt))
            conn.commit()
            client_conn.send("signup_success".encode())
        else:
            client_conn.send("signup_failed".encode())

    @staticmethod
    def handel_login(data, client_conn: socket):
        username, password = data.split('/')

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        if is_user_exist(username, cursor):
            cursor.execute("SELECT salt FROM users WHERE username = ?", (username,))
            salt = cursor.fetchone()[0]

            password_hash = hashing(password, salt)

            cursor.execute("SELECT Password FROM users WHERE username = ?", (username,))
            db_password = cursor.fetchone()[0]
            if password_hash == db_password:
                cursor.execute("SELECT FirstName, LastName FROM users WHERE username = ?", (username,))
                result = cursor.fetchall()
                user = result[0]
                first = user[0]
                last = user[1]

                client_conn.send(f"login_success:{first}:{last}".encode())
            else:
                client_conn.send("login_failed".encode())
        else:
            client_conn.send("login_failed".encode())

    def start(self):
        print("[LISTENING]")
        while True:
            conn, addr = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(Client(addr, conn),))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == '__main__':
    Server()

import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
import sqlite3
from hashlib import sha256
import os

pepper = "yoav123"


def hashing(text, salt):
    """
    hashing the data
    :param text: text to hash
    :param salt: random bytes
    :return: hashed data
    """
    # pepper is a global variable
    global pepper
    # adding salt and pepper
    data = salt + text.encode() + pepper.encode()
    # hashing the data 10 time to make it safer
    for _ in range(10):
        data = sha256(data).digest()
    return data


def make_keys():
    """
    generating the rsa keys
    :return: private key and public key
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


class Client:
    def __init__(self, addr, conn):
        self.username = None

        self.addr = addr
        self.conn = conn
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        self.private_key, public_key = make_keys()
        self.public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.public_key = None

    def decrypt(self, encrypted_text):
        """
        :param encrypted_text:
        :return: the decrypted text
        """
        decrypted_message = self.private_key.decrypt(
            encrypted_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_message

    def encrypt(self, text):
        """
        :param text:
        :return: the encrypted text
        """
        try:
            text = text.encode()
        except:
            pass

        encrypted_text = self.public_key.encrypt(
            text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))
        return encrypted_text


def is_user_exist(username, cursor: sqlite3.Cursor):
    """
    check if the user exists in the database based on username
    :param username:
    :param cursor: sqlite3 cursor
    :return: boolean
    """
    cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    return cursor.fetchone() is not None


class Server:
    def __init__(self, host="127.0.0.1", port=1234):
        self.clients = []
        self.allow_list = []
        self.control_list = []
        self.connected = True

        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print("[STARTING]")
        self.start()

    def handle_client(self, client: Client):
        """
        handle client actions and messages
        :param client: client object
        :return: none
        """
        print("[NEW CONNECTION]")
        self.clients.append(client)

        client.conn.send(client.public_key_pem)
        public_key_pem = client.conn.recv(4096)
        client.public_key = load_pem_public_key(public_key_pem)

        signed = False
        connected = True
        while self.connected and connected:
            try:
                msg = client.conn.recv(1024)
                msg = client.decrypt(msg).decode()
                header, data = msg.split(":")

                if header == "exit":
                    connected = True
                if not signed:
                    if header == "signup":
                        signed = self.handel_signup(data, client)
                    elif header == "login":
                        signed = self.handel_login(data, client)
                else:
                    if header == "allow":
                        self.allow_list.append(client)
                    if header == "ExitAllow":
                        self.allow_list.remove(client)
                    if header == "control":
                        username = data  # Username being requested for control
                        names = []  # List to hold usernames of allowed clients
                        response = "bad"  # Default response is "bad" (not allowed)

                        # Collect usernames from allowed clients
                        for allow_client in self.allow_list:
                            names.append(allow_client.username)

                        # If requested username is in the list of allowed usernames
                        if username in names:
                            # Find the corresponding client object
                            for allow_client in self.allow_list:
                                if allow_client.username == username:
                                    # Send encrypted control request to the allowed client
                                    msg = allow_client.encrypt(client.username)
                                    allow_client.conn.send(msg)
                                    response = "good"  # Mark response as "good" if found

                        # Send encrypted response back to the requesting client
                        encrypted = client.encrypt(response)
                        client.conn.send(encrypted)

                    # Handle "choose" header: one client is accepting or denying a control request
                    if header == "choose":
                        action, username = data.split(',')  # Action ("accept"/"deny") and username of other client
                        other_client = self.get_user_by_username(username)  # Get the client object by username

                        if other_client:
                            if action == "accept":
                                key = os.urandom(32)  # Generate a 256-bit encryption key

                                # Notify the other client that the request is accepted and send connection details
                                text = other_client.encrypt("accept:" + client.addr[0])
                                other_client.conn.send(text)
                                other_client.conn.send(other_client.encrypt(key))

                                # Send the same info (IP and key) to the requesting client
                                client.conn.send(client.encrypt(other_client.addr[0]))
                                client.conn.send(client.encrypt(key))

                            if action == "deny":
                                # Notify the other client that the request was denied
                                text = other_client.encrypt("deny:")
                                other_client.conn.send(text)

            except Exception:
                connected = False
        print(f"[DISCONNECT]")
        try:
            self.clients.remove(client.conn)
            self.allow_list.remove(client)
            self.control_list.remove(client)
            client.conn.close()
        except Exception:
            pass

    def get_user_by_username(self, username) -> Client:
        """
        finding other client
        :param username: username of wanted client
        :return: a client object
        """
        for client in self.clients:
            if client.username == username:
                return client

    @staticmethod
    def handel_signup(data, client):
        """
        :param data: user personal data
        :param client: client object
        :return: boolean
        """
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
            client.username = username
            client.conn.send(client.encrypt("signup_success"))
            return True
        else:
            client.conn.send(client.encrypt("signup_failed"))
            return False

    @staticmethod
    def handel_login(data, client):
        """
        :param data: user data input
        :param client: client object
        :return: boolean
        """
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

                client.username = username

                client.conn.send(client.encrypt("login_success:{first}:{last}"))
                return True
            else:
                client.conn.send(client.encrypt("login_failed"))
                return False
        else:
            client.conn.send(client.encrypt("login_failed"))
            return False

    def start(self):
        """
        starting the server and listening for connections
        :return: none
        """
        print("[LISTENING]")
        while True:
            conn, addr = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(Client(addr, conn),))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == '__main__':
    Server("10.100.102.20")

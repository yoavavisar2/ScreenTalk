import socket
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def make_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


class LoggedUser:
    def __init__(self):
        self.first_name = None
        self.second_name = None
        self.username = None

    def logged(self, first, second, username):
        self.first_name = first
        self.second_name = second
        self.username = username


class Client(LoggedUser):
    def __init__(self, host='127.0.0.1', port=1234):
        super().__init__()
        self.host = host
        self.port = port

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        public_key_pem = self.client.recv(1024)
        self.public_key = load_pem_public_key(public_key_pem)

        self.private_key, public_key = make_keys()
        self.public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.client.send(self.public_key_pem)

    def encrypt(self, text):
        encrypted_text = self.public_key.encrypt(text.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                             algorithm=hashes.SHA256(), label=None))
        return encrypted_text

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

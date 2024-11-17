import socket
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Client:
    def __init__(self, host='127.0.0.1', port=1234):
        self.host = host
        self.port = port

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.public_key_pem = self.client.recv(1024)
        self.public_key = load_pem_public_key(self.public_key_pem)

    def encrypt(self, text):
        encrypted_text = self.public_key.encrypt(text.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                             algorithm=hashes.SHA256(), label=None))
        return encrypted_text

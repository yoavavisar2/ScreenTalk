import socket
import threading

class Client:
    def __init__(self, addr, conn):
        self.addr = addr
        self.conn = conn


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
        connected = True
        while connected:
            try:
                msg = client.conn.recv(1024).decode("utf-8")
                if msg:
                    print(f"[{client.addr}] {msg}")
                    client.conn.send("Message received".encode("utf-8"))
                else:
                    connected = False
            except:
                connected = False

        print(f"[DISCONNECT]")
        try:
            self.clients.remove(client.conn)
            client.conn.close()
        except:
            pass

    def start(self):
        print("[LISTENING]")
        while True:
            conn, addr = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(Client(addr, conn),))
            client_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == '__main__':
    Server()

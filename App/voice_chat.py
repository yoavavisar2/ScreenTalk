from vidstream import AudioSender, AudioReceiver
import threading


class VoiceChat:
    def __init__(self, local_ip, remote_ip, port):
        self.receiver = AudioReceiver(local_ip, port)
        self.sender = AudioSender(remote_ip, port)

        self.receiver_thread = threading.Thread(target=self.receiver.start_server)
        self.sender_thread = threading.Thread(target=self.sender.start_stream)

    def start(self):
        self.receiver_thread.start()
        self.sender_thread.start()

    def stop(self):
        self.receiver.stop_server()
        self.sender.stop_stream()

        self.receiver_thread.join()
        self.sender_thread.join()

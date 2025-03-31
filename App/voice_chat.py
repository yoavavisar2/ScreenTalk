from vidstream import AudioSender, AudioReceiver
import threading


def voiceChat(local, remote, port):
    receiver = AudioReceiver(local, port)
    threading.Thread(target=receiver.start_server)

    sender = AudioSender(remote, port)
    threading.Thread(target=sender.start_stream)

from socket import socket, AF_INET, SOCK_DGRAM
from threading import Timer

class Client_Heartbeat():
    def __init__(self, ipaddress, port):
        self.ipaddress = ipaddress
        self.port = port
        self.start_time = None
        self.sock = socket(AF_INET, SOCK_DGRAM)

    def send_beat(self, message):
        self.sock.sendto(message, (self.ipaddress, self.port))
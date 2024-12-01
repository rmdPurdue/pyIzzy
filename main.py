# Heartbeat thread
# Communication thread
# Sensor readings thread
# Movement thread
import socket
import time
import threading
from communication.heartbeat.client import Client_Heartbeat
from communication.heartbeat.heartbeat_message import HeartbeatMessage
from queue import Queue
from communication.ports import Ports
from devices.server import Server

in_heartbeat_message = Queue()
mother = Server()

def main():
    #have to create thread to listen for messages
    heartbeat_thread = threading.Thread(target=heartbeat, args=(in_heartbeat_message, "192.168.1.10",8080))
    heartbeat_thread.start()
    heartbeat_thread.join()

def incoming_heartbeat(incoming_message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", Ports.UDP_RECEIVE_PORT.value))
    message = HeartbeatMessage()
    while True:
        data, remote_ip = sock.recvfrom(1024)
        mother.ip_address = remote_ip
        if message.process_packet(data):
            incoming_message.put(message, block=False)
        else:
            pass
        # If so, can I collect Mother UUID here, too?
        # Can this be modified to confirm it's the correct mother?

def heartbeat(incoming_message, ipaddress, port):
    if not incoming_message.empty():
        message = incoming_message.get()

    # This should check for a message on in_heartbeat_message Queue
    # and pull if message is new.
    # should confirm how long since last message
    # should send a reply based on current status.
    # where is current status set?
    beat = Client_Heartbeat(ipaddress, port)
    message = HeartbeatMessage()
    while True:
        beat.send_beat(message)
        time.sleep(2)

if __name__ == '__main__':
    main()

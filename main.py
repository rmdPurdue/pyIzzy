# Heartbeat thread
# Communication thread
# Sensor readings thread
# Movement thread
import socket
import logging
import time
import threading
from smbus2 import SMBus

from ads1115.ads1115 import ADS1115
from line_follower.line_sensor import LineSensor
from communication.heartbeat.client import Client_Heartbeat
from communication.heartbeat.heartbeat_message import HeartbeatMessage
from queue import Queue
from communication.ports import Ports
from devices.server import Server
from kangaroo.kangaroo_channel import KangarooChannel
from kangaroo.kangaroo_serial import KangarooSerial

in_heartbeat_message = Queue()
mother = Server()
SENSOR_SPACING = 13
SENSOR_WIDTH = 17
SENSOR_Y_DISTANCE = 88

def main():
    logger = logging.getLogger('pyIzzy')
    logging.basicConfig(filename='pyIzzy.log', level=logging.DEBUG)
    logger.info('Izzy started.')
    running = True

    # Heartbeat thread
    #heartbeat_thread = threading.Thread(target=heartbeat, args=(in_heartbeat_message, "192.168.1.10",8080))
    #heartbeat_thread.start()
    #heartbeat_thread.join()

    # Start obstacle detection

    # Start line sensors using ADS1115 interface board
    i2c = SMBus(1)
    ads1115_address = 0x49
    ads1115 = ADS1115
    line_sensor_left = LineSensor(32000, 2, "DistanceSensor-A2", ads1115) # left
    line_sensor_right = LineSensor(32000, 0, "DistanceSensor-A0", ads1115) # right
    line_sensors = [line_sensor_left, line_sensor_right, SENSOR_SPACING, SENSOR_WIDTH, SENSOR_Y_DISTANCE]

    # Connect to motion controller
    # Open serial connection to Kangaroo Backpack
    drive_controller = KangarooSerial()
    drive_channel = KangarooChannel(drive_controller, 'D')
    turn_channel = KangarooChannel(drive_controller, 'T')

    # Follow line: (traceback through movement/lineFollowing/IZZYMoveLineFollow.java


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

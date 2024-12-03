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
from line_sensor.line_sensor import LineSensor
from movement.line_follower import LineFollower
from communication.heartbeat.client import Client_Heartbeat
from communication.heartbeat.heartbeat_message import HeartbeatMessage
from queue import Queue
from communication.ports import Ports
from devices.server import Server
from kangaroo.kangaroo_channel import KangarooChannel
from kangaroo.kangaroo_serial import KangarooSerial

in_heartbeat_message = Queue()
mother = Server()
WHEEL_RADIUS = 67.3 # mm
SYSTEM_RADIUS = 124.5 # mm
ENCODER_RESOLUTION = 20 # ticks/rev
MOTOR_RATIO = 100
SENSOR_SPACING = 13 # mm
SENSOR_WIDTH = 17 # mm
SENSOR_Y_DISTANCE = 88 # mm

def main():
    logger = logging.getLogger('pyIzzy')
    logging.basicConfig(filename='pyIzzy.log', level=logging.DEBUG)
    logger.info('Izzy started.')
    running = True

    # Heartbeat thread
    #heartbeat_thread = threading.Thread(target=heartbeat, args=(in_heartbeat_message, "192.168.1.10",8080))
    #heartbeat_thread.start()
    #heartbeat_thread.join()

    # Connect to motion controller
    # Open serial connection to Kangaroo Backpack
    drive_controller = KangarooSerial()
    drive_channel = KangarooChannel(drive_controller, 'D')
    turn_channel = KangarooChannel(drive_controller, 'T')

    # Start line sensors using ADS1115 interface board
    i2c = SMBus(1)
    ads1115_address = 0x49
    ads1115 = ADS1115(i2c, ads1115_address)
    line_sensor_left = LineSensor(32000, 2, "DistanceSensor-A2", ads1115) # left
    line_sensor_right = LineSensor(32000, 0, "DistanceSensor-A0", ads1115) # right
    line_sensors = [line_sensor_left, line_sensor_right, SENSOR_SPACING, SENSOR_WIDTH, SENSOR_Y_DISTANCE]

    # Follow line
    line_follower = LineFollower()
    line_follower.setup(WHEEL_RADIUS, SYSTEM_RADIUS, ENCODER_RESOLUTION, MOTOR_RATIO)
    line_follower.pid_setup(line_sensors, 1, 0, 0)
    line_follower.set_channels(drive_channel, turn_channel)
    line_follower.update_speed(100)
    line_follower.start_following()
    line_follower.follow_line()

    # Start obstacle detection

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

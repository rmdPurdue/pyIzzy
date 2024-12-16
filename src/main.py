import logging
from typing import Any, List

import ADS1x15
import serial
from pythonosc.udp_client import SimpleUDPClient
from src.communication.osc_addresses import OSCAddresses
from src.devices.client import Izzy
from src.line_sensor.analog_input import AnalogIn
from src.line_sensor.line_sensor import LineSensor
from src.line_sensor.line_follower import LineFollower
from src.communication.ports import Ports
from src.kangaroo.kangaroo_channel import KangarooChannel
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio

from src.line_sensor.sensor_array import SensorArray
from src.movement.drive_movement import DriveMovement

# in_heartbeat_message = Queue()
# mother = Server()
KANGAROO_PORT = "/dev/ttyS0"
physical_details = {"wheel radius": 67.3 / 2,
                    "system radius": 124.5,
                    "sensor y offset": 88,
                    "encoder resolution": 20,
                    "motor ratio": 100,
                    }
MY_IP_ADDRESS = "127.0.0.1"  # IZZY's IP; don't use local host
MOTHER_IP_ADDRESS = "192.168.1.1"  # Mother's IP
ads1115_address = 0x49
izzy = Izzy()

# Start logger
logger = logging.getLogger(__name__)
log_console_handler = logging.StreamHandler()
log_file_handler = logging.FileHandler('pyIzzy.log',
                                       mode="a",
                                       encoding="utf-8")
logger.addHandler(log_console_handler)
logger.addHandler(log_file_handler)
formatter = logging.Formatter("{asctime} - {levelname} - {message}",
                              style="{",
                              datefmt="%Y-%m-%d %H:%M")
log_console_handler.setFormatter(formatter)
log_file_handler.setFormatter(formatter)
logger.setLevel(10)
logger.info('Izzy started.')

# Open serial connection to Kangaroo Backpack motion controller
drive_controller = serial.Serial(KANGAROO_PORT,
                                 timeout=0,
                                 baudrate=9600,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE)
drive_channel = KangarooChannel(drive_controller, 'D')
logger.info("Created drive channel.")
turn_channel = KangarooChannel(drive_controller, 'T')
logger.info("Created turn channel.")

# Start line sensors using ADS1115 interface board
ads1115 = ADS1x15.ADS1115(1, ads1115_address)
ads1115.setGain(1)
ads1115.setMode(ads1115.MODE_SINGLE)
logger.info("Created ADS115 instance.")
left_line_sensor = LineSensor(AnalogIn(ads1115, 1))
logger.info("Created left line sensor.")
right_line_sensor = LineSensor(AnalogIn(ads1115, 3))
logger.info("Created right line sensor.")
sensor_array = SensorArray(izzy.sensor_y_offset,
                           left_line_sensor,
                           right_line_sensor)
logger.info("Created sensor array.")

# Initialize Line Follower
line_follower = LineFollower()
# logger.info("Created line follower/movement controller.")
# line_follower.setup(WHEEL_RADIUS, SYSTEM_RADIUS, ENCODER_RESOLUTION,
# MOTOR_RATIO)
# line_follower.pid_setup(line_sensors, 1, 0, 0)
# line_follower.set_channels(drive_channel, turn_channel)
# logger.info("Set movement channels.")
# line_follower.update_speed(100)
# line_follower.start_following()

"""
# Initialize Obstacle Responder
obstacle_responder = ObstacleResponder()
"""

# Initialize OSC client to talk to Mother
izzy_udp = SimpleUDPClient(MOTHER_IP_ADDRESS, Ports.OSC_SEND_PORT.value)

# movement test
mover = DriveMovement(izzy)
logger.info("Set movement channels.")
mover.set_channels(drive_channel, turn_channel)
logger.info("Sending undetectable turn command to initiate movement controls.")
mover.turn_channel.p(1)  # Kangaroo seems to need a tiny turn command before accepting drive commands


# OSC Message Callback functions
def follow_line_state(address: str, *args: List[Any]):
    # we expect one string argument and one speed argument
    if not len(args) == 2 or type(args[0]) is not str or type(
            args[1]) is not int:
        return
    if args[0] == 'start': line_follower.set_moving_state(True)
    if args[0] == 'stop': line_follower.set_moving_state(False)
    line_follower.update_speed(args[1])


def follow_line_speed(address: str, *args: List[Any]):
    # we expect one speed argument
    if not len(args) == 1 or type(args[0]) is not int:
        return
    line_follower.update_speed(args[0])


def follow_line_tune(address: str, *args: List[Any]):
    if not len(args) == 3 or type(args[0]) is not int or type(
            args[1]) is not int or type(args[2]) is not int:
        return
    line_follower.tune_pid_loop(args[0], args[1], args[2])


def follow_line_threshold(address: str, *args: List[Any]):
    if not len(args) == 2 or type(args[0]) is not int or type(
            args[1]) is not int:
        return
    # line_sensors[0].threshold = args[0]
    # line_sensors[1].threshold = args[1]


def follow_line_sensor_ranges(address: str, *args: List[Any]):
    if not len(args) == 4 or type(args[0]) is int or type(
            args[1]) is not int or type(args[2]) is not int or type(
        args[3]) is not int:
        return
    # line_sensors[0].set_min_reading(args[0])
    # line_sensors[2].set_max_reading(args[1])
    # line_sensors[1].set_min_reading(args[2])
    # line_sensors[1].set_max_reading(args[3])


def follow_line_reset_system(address: str, *args: List[Any]):
    if not len(args) == 0:
        return
    line_follower.reset_system()


def follow_line_soft_estop(address: str, *args: List[Any]):
    if not len(args) == 1 or type(args[0]) is not str:
        return
    if args[0] == 'eStop':
        line_follower.soft_estop()


# Initialize OSC message dispatcher
osc_dispatcher = Dispatcher()

# Assign OSC message callback functions for incoming commands
osc_dispatcher.map(OSCAddresses.FOLLOW_LINE_SPEED, follow_line_state)
osc_dispatcher.map(OSCAddresses.FOLLOW_LINE_SPEED, follow_line_speed)
osc_dispatcher.map(OSCAddresses.FOLLOW_LINE_TUNE, follow_line_tune)
osc_dispatcher.map(OSCAddresses.FOLLOW_LINE_THRESHOLD, follow_line_threshold)
osc_dispatcher.map(OSCAddresses.FOLLOW_LINE_SET_SENSOR_RANGES,
                   follow_line_sensor_ranges)
osc_dispatcher.map(OSCAddresses.FOLLOW_LINE_RESET_SYSTEM,
                   follow_line_reset_system)
osc_dispatcher.map(OSCAddresses.FOLLOW_LINE_SOFT_ESTOP, follow_line_soft_estop)


async def loop():
    # logger.debug("Send move command, 20 rotations at speed 20.")
    # mover.move(2, 20)

    while True:
        logger.debug("Read line sensor2.")
        logger.debug(f"Sensor 1 Reading: {ads1115.readADC(1)}")
        logger.debug(f"Sensor 2 Reading: {ads1115.readADC(3)}")
        running = True

        # Heartbeat thread
        # heartbeat_thread = threading.Thread(target=heartbeat,
        # args=(in_heartbeat_message, "192.168.1.10",8080))
        # heartbeat_thread.start()
        # heartbeat_thread.join()

        # Start listening for command messages

        # Follow line
        # line_follower.follow_line()

        # Start obstacle detection
        # obstacle_responder.start_avoiding()

        # Send data update to Mother
        # message = OscMessageBuilder(address="/Mother/Status")
        # message.add_arg(line_follower.current_speed)
        # message.add_arg(line_follower.pid.get_pid_value())
        # message.add_arg(line_follower.pid.get_error_angle())
        # message.add_arg(line_follower.pid.get_kp())
        # message.add_arg(line_follower.pid.get_ki())
        # message.add_arg(line_follower.pid.get_kd())
        # message.add_arg(line_follower.get_moving_state())
        # message.add_arg(line_sensor_left.get_reading())
        # message.add_arg(0) # we have no center sensor any longer
        # message.add_arg(line_sensor_right.get_reading())
        # message.add_arg(line_sensor_left.get_threshold())
        # message.add_arg(0) # we have no center sensor any longer
        # message.add_arg(line_sensor_right.get_threshold())
        # message.add_arg(drive_channel.get_p())
        # message.add_arg(drive_channel.get_s())
        # message.add_arg(turn_channel.get_p())
        # message.add_arg(turn_channel.get_s())
        # message = message.build()
        # izzy.send(message)

        await asyncio.sleep(
            0.2)  # sleep for a tenth of a second to let the OSC server
        # listen for messages.


async def init_main():
    # Start asynchronous OSC server
    osc_server = AsyncIOOSCUDPServer(
        (MY_IP_ADDRESS, Ports.OSC_RECEIVE_PORT.value),
        osc_dispatcher, asyncio.get_event_loop())
    transport, protocol = await osc_server.create_serve_endpoint()

    await loop()

    transport.close()


"""
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
"""

if __name__ == '__main__':
    asyncio.run(init_main())
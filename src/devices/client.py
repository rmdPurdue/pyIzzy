import math
import socket
import struct

from src.communication.heartbeat.client_status import IZZYStatus


# TODO: add uuid, status, and lastContact to attributes
#  docstring.

class Izzy:
    """
    A class to store status information about IZZY.

    Attributes
    ----------
    ip_address: str
        a string representation of the IP address of the unit

    wheel_radius: float
        the radius of a drive wheel, in mm

    system_radius: float
        the distance from the center of the unit to the outer edge of a drive
        wheel, in mm.

    line_sensor_y_offset: int
        the distance from the center of the unit to the middle of the line
        sensor array, in mm.

    encoder_resolution: int
        the number of encoder counts for one revolution of the motor drive
        shaft.

    motor_ratio: int
        the gearbox reduction ratio

    line_following: boolean
        true when line_following mode is active

    moving: boolean
        true when unit is in motion

    position: x: int, y: int, z: int
        a tuple holding the current relative x,y,z position of the unit

    heading: int
        the relative current heading of the unit in degrees

    speed: int
        the current speed of the unit

    drive_resolution: int
        the resolution of the motor wheels, in encoder ticks per centimeter
        of straight-line travel

    turn_resolution: int
        the resolution of the motor wheels, in encoder ticks per degree of turn
    """

    name = None
    uuid = None
    ip_address = IPAddr = socket.gethostbyname(socket.gethostname())
    status = IZZYStatus.AVAILABLE.value
    lastContact = None
    wheel_radius = 67.3 / 2
    system_radius = 124.5
    line_sensor_y_offset = 88
    encoder_resolution = 20
    motor_ratio = 100
    position = {"x": 1, "y": 2, "z": 3}
    heading = 4
    speed = 5
    drive_resolution = int(math.pi * wheel_radius * 2 * encoder_resolution *
                           motor_ratio)
    turn_resolution = int(math.pi / 180 * system_radius * drive_resolution)

    def __init__(self, uuid, name):
        self.name = name
        self.uuid = uuid
        self.drive_units = f"1 centimeter = {self.drive_resolution} ticks"
        self.turn_units = f"1 degree = {self.turn_resolution} ticks"

    def build_status_message(self):
        data = bytearray()
        delimiter = ",".encode()

        for byte in self.name.encode():
            data.append(byte)
        data.append(delimiter[0])
        data.append(self.status)
        data.append(delimiter[0])
        for byte in self.position["x"].to_bytes(2):
            data.append(byte)
        data.append(delimiter[0])
        for byte in self.position["y"].to_bytes(2):
            data.append(byte)
        data.append(delimiter[0])
        for byte in self.position["z"].to_bytes(2):
            data.append(byte)
        data.append(delimiter[0])
        for byte in self.heading.to_bytes(2):
            data.append(byte)
        data.append(delimiter[0])
        for byte in self.speed.to_bytes(2):
            data.append(byte)
        return data

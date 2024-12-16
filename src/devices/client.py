import math


class Izzy:
    """
    A class to store status information about IZZY.

    Attributes
    ----------
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

    ip_address: str
        a string representation of the IP address of the unit

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

    wheel_radius = 67.3 / 2
    system_radius = 124.5
    line_sensor_y_offset = 88
    encoder_resolution = 20
    motor_ratio = 100
    ip_address = "127.0.0.1"  # IZZY's IP; don't use local host
    line_following = False
    moving = False
    position = {"x": 0, "y": 0, "z": 0}
    heading = 0
    speed = 0
    drive_resolution = int(math.pi * wheel_radius * 2 * encoder_resolution *
                           motor_ratio)
    turn_resolution = int(math.pi / 180 * system_radius * drive_resolution)

    def __init__(self):
        self.drive_units = f"1 centimeter = {self.drive_resolution} ticks"
        self.turn_units = f"1 degree = {self.turn_resolution} ticks"

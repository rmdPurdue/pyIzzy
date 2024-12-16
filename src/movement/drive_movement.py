import math

from multimethod import multimethod


class DriveMovement:
    """
    A class to handle movement commands for the unit.

    Attributes
    ----------
    izzy: a client object
        the client object for this unit

    drive_channel: a kangaroo_channel object
        the drive channel for this unit

    turn_channel: a kangaroo_channel object
        the turn channel for this unit

    Methods
    -------
    set_channels(drive_channel, turn_channel):
        initialize the drive and turn channels of the motion controller

    turn(target_angle)
        turn the unit to the target angle at the current turn speed

    turn(target_angle, speed) @multimethod
        turn the unit to the target angle at the supplied speed

    increase_turn_angle(angle_increment)
        increase the current angle of the unit at the current turn speed
        (positive is CW, negative is CCW)

    increase_turn(angle_increment, speed) @multimethod
        increase the current angle of the unit at the supplied speed
        (positive is CW, negative is CCW)

    set_speed(speed)
        set the current speed of the unit

    increase_speed(speed)
        increase the current speed of the unit by the supplied amount

    move(distance, speed)
        move the distance supplied at the current heading at the
        supplied speed; store the new current position

    soft_estop
        power down drive and turn channels

    reset_drive
        reset parameters to initial settings by calling "set_channels"
    """

    def __init__(self, izzy):
        """
        :param izzy: an izzy client object
        """
        self.izzy = izzy
        self.turn_channel = None
        self.drive_channel = None

    def set_channels(self, drive_channel, turn_channel):
        """
        Initialize the drive and turn channels of the motion controller.

        :param drive_channel: kangaroo_channel object for the drive channel
        :param turn_channel:  kangaroo_channel object for the turn channel
        """
        self.drive_channel = drive_channel
        self.turn_channel = turn_channel
        self.drive_channel.start()
        self.turn_channel.start()
        self.drive_channel.units(self.izzy.drive_units)
        self.turn_channel.units(self.izzy.turn_units)

    @multimethod
    def turn(self, target_angle):
        """
        Turn the unit to the target angle at the current turn speed.

        :param target_angle: an angle to turn to, in degrees
        """
        self.turn_channel.p(target_angle)
        self.izzy.heading = target_angle

    @multimethod
    def turn(self, target_angle, speed):
        """
        Turn the unit to the target angle at the supplied speed.

        :param target_angle: an angle to turn to, in degrees
        :param speed: the speed at which to turn
        """
        self.turn_channel.p(target_angle, speed)
        self.izzy.heading = target_angle

    @multimethod
    def increase_turn(self, angle_increment):
        """
        Increase the current angle of the unit at the current turn speed.

        :param angle_increment: the number of degrees to increase the angle by
        """
        self.turn_channel.pi(angle_increment)
        self.izzy.heading += angle_increment

    @multimethod
    def increase_turn(self, angle_increment, speed):
        """
        Increase the current angle of the unit at the supplied speed.

        :param angle_increment: the number of degrees to increase the turn by
        :param speed: the speed at which to turn
        """
        self.turn_channel.pi(angle_increment, speed)
        self.izzy.heading += angle_increment

    def set_speed(self, speed):
        """
        Set the current speed of the unit.

        :param speed: a speed set point value
        """
        self.izzy.speed = speed
        self.drive_channel.s(speed)

    def increase_speed(self, speed):
        """
        Increase the current speed of the unit by the supplied amount.

        :param speed: an amount to increase the speed by
        """
        self.izzy.speed += speed
        self.drive_channel.si(self.izzy.speed)

    def move(self, distance, speed):
        """
        Move the distance supplied at the current heading at the
        supplied speed; store the new current position.

        :param distance: a distance to move
        :param speed: a speed to move at
        """
        self.izzy.speed = speed
        self.izzy.position["x"] += distance * math.cos(self.izzy.heading)
        self.izzy.position["y"] += distance * math.sin(self.izzy.heading)
        self.drive_channel.pi(distance, speed)

    def soft_estop(self):
        """Power down drive and turn channels."""
        self.drive_channel.power_down()
        self.turn_channel.power_down()
        self.izzy.speed = 0

    def reset_drive(self):
        """Reset parameters to initial settings by calling 'set_channels'."""
        self.set_channels(self.drive_channel, self.turn_channel)


"""
    def simple_move(self, target_position, angle_direction):
        if self.current_position["x"] == target_position["x"] and self.current_position["y"] != target_position["y"]:
            cw_angle = 90
            ccw_angle = 270
        else:
            tan_angle = math.tan(self.current_position["y"] / (self.current_position["x"] * 360 / (2 * math.pi)))
            if target_position["x"] > self.current_position["x"]:
                if target_position["y"] > self.current_position["y"]:
                    ccw_angle = tan_angle
                    cw_angle = 360 - tan_angle
                else:
                    ccw_angle = 360 - tan_angle
                    cw_angle = tan_angle
            else:
                if target_position["y"] > self.current_position["y"]:
                    ccw_angle = 180 - tan_angle
                    cw_angle = 180 + tan_angle
                else:
                    ccw_angle = 180 + tan_angle
                    cw_angle = 180 - tan_angle
        if angle_direction == 1:
            self.turn(-cw_angle)
        elif angle_direction == -1:
            self.turn(ccw_angle)
        else:
            if abs(self.angle - ccw_angle) > abs(self.angle - cw_angle):
                self.turn(-cw_angle)
            else:
                self.turn(ccw_angle)
        distance = math.sqrt(pow(self.current_position["x"], 2) + pow(self.current_position["y"], 2))
        self.move(distance, 10)
        self.current_position = target_position
"""

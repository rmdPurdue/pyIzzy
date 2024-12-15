import logging
import time

from multimethod import multimethod


class KangarooChannel:
    """
    A class used to represent a control channel on a Kangaroo x2 Serial
    Backpack by Dimension Engineering. Based loosely off the Arduino
    libraries for simple serial control provided by the manufacturer.

    Attributes
    ----------
    kangaroo_serial: serial object
        a serial object passed to the class at instantiation.

    name: str
        a single character representing the name of the control channel,
        passed to the class at instantiation. Can be 'D' (drive) or 'T' (
        turn) for mixed mode motor control of two motors, or '1' or '2' for
        independent mode motor control of (up to) two motors.

    Methods
    -------
    get_name -> str
        returns the name of the channel

    p(units: int)
        creates a message to move the channel to the given absolute position

    p(units: int, speed: int) @multimethod
        creates a message to move the channel to the given absolute position
        at the given speed

    s(units: int)
        creates a message to move the channel at the given absolute speed

    pi(units: int)
        creates a message to move the channel a given distance from its
        current position

    pi(units: int, speed: int) @multimethod
        creates a message to move the channel a given distance from its
        current position at the given speed

    si(units: int)
        creates a message to increase the speed of the channel by the given
        amount

    units(units: str)
        creates a message to set a ratio for a user-friendly unit to the
        machine-side units used for position/velocity control

    get_s -> str
        creates a message to request the current speed of the channel

    get_p -> str
        creates a message to request the current position of the channel

    start
        creates a message to powerup the control channel

    powerdown
        creates a message to powerdown the control channel

    write(command: str) -> str
        sends the command message; returns a response message, if any
    """

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

    def __init__(self, kangaroo_serial, name):
        """
        :param kangaroo_serial: a serial object
        :param name: the name of the channel
        """

        self.kangaroo_serial = kangaroo_serial
        self.name = name

    def get_name(self):
        """
        :return: the string name of the channel
        """

        return self.name

    @multimethod
    def p(self, units: int):
        """
        Creates a message to move the channel to the given absolute
        position, in the hardware units defined at setup ("lines"
        or "ticks" of an encoder, for example) or the units as defined by a
        "units" command. Calls the write method to send the message via serial
        communication.

        :param units: the absolute position to travel to; int;
        """

        command = f'{self.name}, p{units}\r\n'
        self.write(command)

    @multimethod
    def p(self, units: int, speed: int):
        """
        Creates a message to move the channel to the given absolute position
        at the given speed, in the hardware units defined at setup ("lines"
        or "ticks" of an encoder, for example) or the units as defined by a
        "units" command. Calls the write method to send the message via
        serial communication.

        :param units: the absolute position to travel to; int
        :param speed: the speed of travel; int
        """

        command = f'{self.name}, p{units} s{speed}\r\n'
        self.write(command)

    def s(self, units):
        """
        Creates a message to move the channel at the given absolute speed,
        in the hardware units defined at setup ("lines" or "ticks" of an
        encoder, for example) or the units as defined by a "units" command.
        Calls the write method to send the message via serial communication.

        :param units: speed to set the channel to; int
        """

        command = f'{self.name}, s{units}\r\n'
        self.write(command)

    @multimethod
    def pi(self, units: int):
        """
        Creates a message to move the channel a given distance from its
        current position, in the hardware units defined at setup ("lines"
        or "ticks" of an encoder, for example) or the units as defined by a
        "units" command. Calls the write method to send the message via
        serial communication.

        :param units: distance to travel; int
        """

        command = f'{self.name}, pi{units}\r\n'
        self.write(command)

    @multimethod
    def pi(self, units: int, speed: int):
        """
        Creates a message to move the channel a given distance from its
        current position at the given speed, in the hardware units defined at
        setup ("lines" or "ticks" of an encoder, for example) or the units as
        defined by a "units" command. Calls the write method to send the
        message via serial communication.

        :param units: distance to travel; int
        :param speed: speed of travel; int
        """

        command = f'{self.name}, pi{units} s{speed}\r\n'
        self.write(command)

    def si(self, units):
        """
        Creates a message to increase the speed of the channel by the given
        amount, in the hardware units defined at setup ("lines"
        or "ticks" of an encoder, for example) or the units as defined by a
        "units" command. Calls the write method to send the message via serial
        communication.

        :param units: amount to increase the speed; int
        """

        command = f'{self.name}, si{units}\r\n'
        self.write(command)

    def units(self, units):
        """
        Creates a message to set a ratio for a user-friendly unit to the
        machine-side units used for position/velocity control. Strings are
        formatted as "x units = y units"; for example, "1 revolution = 500
        lines." Only the numerical values matter; the text is for human
        readability. Machine units are dependent on the setup of the hardware.
        Calls the write method to send the message via serial communication.

        :param units: a string ratio of user units to machine units; str
        """

        command = f'{self.name}, units {units}\r\n'
        self.write(command)

    def get_s(self):
        """
        Creates a message to request the current speed of the channel,
        in the hardware units defined at setup ("lines" or "ticks" of an
        encoder, for example) or the units as defined by a "units" command.
        Calls the write method to send the message via serial communication and
        returns the current speed.

        :return: the current speed; int
        """

        command = f'{self.name}, gets\r\n'
        return self.write(command)

    def get_p(self):
        """
        Creates a message to request the current position of the channel,
        in the hardware units defined at setup ("lines" or "ticks" of an
        encoder, for example) or the units as defined by a "units" command.
        Calls the write method to send the message via serial communication
        and returns the current position.

        :return: the current position; int
        """

        command = f'{self.name}, getp\r\n'
        return self.write(command)

    def start(self):
        """
        Creates a message to powerup the control channel. Must be called
        before any movement commands will be followed. Calls the write
        method to send the message via serial communication.
        """

        command = f'{self.name}, start\r\n'
        self.write(command)

    def power_down(self):
        """
        Creates a message to powerdown the control channel. Calls the write
        method to send the message via serial communication.
        """

        command = f'{self.name}, powerdown\r\n'
        self.write(command)

    def write(self, command):
        """
        Confirms that the serial communication is open for writing and sends
        the command message. Waits a tenth of a second and checks for a
        response message. If there is, reads it and returns the message.

        :param command: a command to send via serial communication; str
        :return: any message returned by the device; ste
        """

        if self.kangaroo_serial.is_open:
            self.kangaroo_serial.write(command.encode())
            self.logger.debug(f"Sent {command} to IZZY.")
            time.sleep(0.1)
            if self.kangaroo_serial.in_waiting > 0:
                reply = self.kangaroo_serial.read(
                    self.kangaroo_serial.in_waiting)
                self.logger.debug(f"Kangaroo returned: {reply}")
                return reply.decode()

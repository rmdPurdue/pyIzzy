import serial
import logging


class SabertoothPacketSerial:
    """A class for sending packet serial commands to a Sabertooth 2x12.

    Hardware address is set on dipswitches on the Sabertooth. Address range is 128 - 135.
    Serial messages follow 8N1 protocol (8 data bytes, no parity bits, one stop bit). Default
    baud rate is 9600, but can be changed using the method below. Note that changed baud rates
    will take effect after a power cycle of the Sabertooth, and that once set they cannot be
    reset to factory defaults; they can only be changed by sending a change baud rate command.

    The packet format for communicating with the Sabertooth comprises an address byte, a command
    byte, a data byte, and a 7-bit checksum. Address bytes are all greater than 128; all subsequent
    bytes are less than 127. This allows multiple devices to share the same serial bus.

    Dip switch settings
    -------------------
                  1     2     3     4     5     6
    Address 128: off | off | on  | on  | on  | on
    Address 129: off | off | on  | off | on  | on
    Address 130: off | off | on  | on  | off | on
    Address 131: off | off | on  | off | off | on
    Address 132: off | off | on  | on  | on  | off
    Address 133: off | off | on  | off | on  | off
    Address 134: off | off | on  | on  | off | off
    Address 135: off | off | on  | off | off | off

    Attributes
    ----------
    sabertooth_port: str
        holds the string for the Linux path to the UART GPIO pins. Default set to "/dev/ttyS0."

    min_voltage: int
        the minimum voltage for the battery powering the Sabertooth.
        Used to set the low threshold of the battery; when set on the Sabertooth,
        if the battery voltage drops below this, outputs will shut down.
        Can be set to values between 0 and 120: 0 = 6v; values step in 0.2V increments (such that
        120 = 30V). Default is 15 (9V for an 11V lipo battery).

    max_voltage: int
        the maximum voltage for the battery powering the Sabertooth. Because the Sabertooth
        incorporates regenerative braking, input voltage will increase when slowing the motor.
        Hardware default is 30V; can be set to a range between 0V and 25V using the formula:
        Value = Desired Volts * 5.12. Default is 56 (for an 11V lipo battery).

    address: int
        the hardware address of the Sabertooth. Default set to 128.

    Methods
    -------



    """

    sabertooth_port = '/dev/ttyS0'
    address = 128
    min_voltage = 9
    max_voltage = 11

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

    def __init__(self, port=sabertooth_port):
        """
        :param port: optional string path to UART port.
        """

        self.my_serial = serial.Serial(port,
                                       timeout=0,
                                       baudrate=9600,
                                       parity=serial.PARITY_NONE,
                                       stopbits=serial.STOPBITS_ONE)

        if port is not self.sabertooth_port:
            self.sabertooth_port = port

        # set_min_voltage
        # set max_voltage

    @staticmethod
    def calculate_checksum(address: int, command: int, value: int) -> int:
        """
        Calculates checksum for a given command sequence.

        :param address: hardware address; int
        :param command: command byte; int
        :param value: value byte; int
        :return: checksum value; int
        """

        return (address + command + value) & 0b01111111

    @staticmethod
    def map(source: int, from_a: int, from_b: int, to_a: int, to_b: int) -> int:
        """
        Maps a value (source) from range from_a to to_a to the range from_b to to_b.

        :param source: value to be remapped; int
        :param from_a: lowest possible value in initial range; int
        :param from_b: lowest possible value in new range; int
        :param to_a: highest possible value in initial range; int
        :param to_b: highest possible value in new range; int
        :return: remapped result; int
        """
        delta_a = from_b - from_a
        delta_b = to_b - to_a
        if delta_a == 0 or delta_b == 0:
            return 0

        scale = delta_b / delta_a
        neg_a = -1 * from_a
        offset = (neg_a * scale) + to_a
        result = int((source * scale) + offset)
        return result

    def write_message(self, address: int, command: int, value: int):
        """
        Sends the sequence of bytes that comprise a command packet.

        :param address: the hardware address of the Sabertooth; int
        :param command: the command prefix; int
        :param value: the value; int
        """

        checksum = self.calculate_checksum(address, command, value)
        self.my_serial.write(self.address.to_bytes())
        self.my_serial.write(command.to_bytes())
        self.my_serial.write(value.to_bytes())
        self.my_serial.write(checksum.to_bytes())

    def set_timeout(self, timeout: int):
        """
        Sets the serial timeout for the Sabertooth; if it does not receive a serial command within
        this amount of time, the driver will shut off. Serial timeout is off by default; a value of
        0 will disable the timeout if it has previously been enabled. Scales at 1 unit per 100ms:
        10 = 1000ms. This setting is not persistent through a power cycle so must be reset if power
        is lost or cycled.

        :param timeout: timeout, in tenths of a second (100 ms).
        """

        command = 14
        value = timeout
        self.write_message(self.address, command, value)

    def set_baud(self, baud: int):
        """
        Sets the baud rate of the Sabertooth. The hardware recognizes four baud rates: 2400, 9600
        19200, and 38400. Any values other than these will default to 9600. This setting is persistent.

        :param baud: a value representing a baud rate, int
        """

        if baud == 2400:
            value = 1
        elif baud == 9600:
            value = 2
        elif baud == 19200:
            value = 3
        elif baud == 38400:
            value = 4
        else:
            value = 2

        command = 15
        self.write_message(self.address, command, value)

    def set_ramping(self, ramp: int) -> float:
        """
        Ramp time is the delay between full forward and full reverse speed. This adjusts or disables
        ramping. Values between 1 and 10 are FAST RAMP; values between 11 and 20 are SLOW RAMP; values
        between 21 and 80 are INTERMEDIATE RAMP. FAST RAMPING is a ramp time of 256/(~1000 x value).
        SLOW and INTERMEDIATE RAMPING are a ramp time of 256/[15.25 x (value - 10)].

        Valid values are 1 to 80

        :param ramp: a ramp setting
        :return: the approximate ramp time in seconds; float
        """

        command = 16
        if ramp is not 0:
            value = ramp
        else:
            value = 1
        self.write_message(self.address, command, value)
        if 0 < ramp <= 10:
            return 256 / (1000 * ramp)
        elif 11 <= ramp <= 80:
            return 256 / (15.25 * (ramp - 10))
        else:
            return 0.25

    def set_deadband(self, deadband: int):
        """
        Sets the extent of the Sabertooth's deadband: the range of commands close to "stop" that
        will be interpreted as stop. This setting is persistent. Range is 0 to 127 and the formula
        is as follows: 127 - value < motors off < 128 + value. A value of 3 would shut the motors
        off with speed commands between 124 (127 - 3) and 131 (128 + 3). A value of 0 resets to
        default, or 3.

        :param deadband: the offset from values of 127 that will mean stop; int
        """

        command = 17
        value = deadband
        self.write_message(self.address, command, value)

    def set_min_voltage(self, voltage: int):
        """
        Sets the minimum voltage for the battery powering the Sabertooth. if the battery voltage drops
        below this, outputs will shut down. Can be set to values between 0 and 120: 0 = 6v; values step
        in 0.2V increments (such that 120 = 30V).

        :param voltage: desired minimum voltage; int
        """
        if self.min_voltage is not voltage:
            self.min_voltage = voltage
        command = 2
        value = self.map(self.min_voltage, 6, 30, 0, 120)
        self.write_message(self.address, command, value)

    def set_max_voltage(self, voltage: int):
        """
        Sets the maximum voltage for the battery powering the Sabertooth. Hardware default is 30V;
        can be set to a range between 0V and 25V using the formula: Value = Desired Volts * 5.12.
        Default is 56 (for an 11V lipo battery).

        :param voltage: desired maximum voltage; int
        """

        if self.max_voltage is not voltage:
            self.max_voltage = voltage
        command = 3
        value = int(self.max_voltage * 5.12)
        self.write_message(self.address, command, value)

    def motor_1_fwd(self, speed: int):
        """
        Used to command motor 1 forward in independent mode. Valid data is 0-127; 0 = off, 127 = full speed.

        :param speed: the speed to set the motor, in range 0% - 100%
        """

        command = 0
        value = self.map(speed, 0, 100, 0, 127)
        self.write_message(self.address, command, value)

    def motor_1_rev(self, speed: int):
        """
        Used to command motor 1 backward in independent mode. Valid data is 0-127; 0 = off, 127 = full speed.

        :param speed: the speed to set the motor, in range 0% - 100%
        """

        command = 1
        value = self.map(speed, 0, 100, 0, 127)
        self.write_message(self.address, command, value)

    def motor_2_fwd(self, speed: int):
        """
        Used to command motor 2 forward in independent mode. Valid data is 0-127; 0 = off, 127 = full speed.

        :param speed: the speed to set the motor, in range 0% - 100%
        """

        command = 4
        value = self.map(speed, 0, 100, 0, 127)
        self.write_message(self.address, command, value)

    def motor_2_rev(self, speed: int):
        """
        Used to command motor 2 backward in independent mode. Valid data is 0-127; 0 = off, 127 = full speed.

        :param speed: the speed to set the motor, in range 0% - 100%
        """

        command = 5
        value = self.map(speed, 0, 100, 0, 127)
        self.write_message(self.address, command, value)

    def drive_motor_1(self, speed: int):
        """
        Used to drive motor 1 either backward or forward, at the cost of resolution of speed. Valid data
        is 0-127; 0 is full reverse, 64 is stop, and 127 is full forward.

        :param speed: the speed to set the motor, in range -100% to 100%
        """

        command = 6
        value = self.map(speed, -100, 100, 0, 127)
        self.write_message(self.address, command, value)

    def drive_motor_2(self, speed: int):
        """
        Used to drive motor 2 either backward or forward, at the cost of resolution of speed. Valid data
        is 0-127; 0 is full reverse, 64 is stop, and 127 is full forward.

        :param speed: the speed to set the motor, in range -100% to 100%
        """

        command = 7
        value = self.map(speed, -100, 100, 0, 127)
        self.write_message(self.address, command, value)

    def drive_fwd(self, speed: int):
        """
        Used to command vehicle forward in mixed mode. Valid data is 0 to 127; 0 = off, 127 = full speed.

        :param speed: the speed to set the motors, in range 0% - 100%
        """

        command = 8
        value = self.map(speed, 0, 100, 0, 127)
        self.write_message(self.address, command, value)

    def drive_rev(self, speed: int):
        """
        Used to command vehicle backward in mixed mode. Valid data is 0-127; 0 = off, 127 = full speed.

        :param speed: the speed to set the motors, in range 0% - 100%
        """

        command = 9
        value = self.map(speed,0,100,0,127)
        self.write_message(self.address, command, value)

    def turn_right(self, speed: int):
        """
        Used to command vehicle to turn right in mixed mode. Valid data is 0-127; 0 = off, 127 = full speed.

        :param speed: the speed to set the motors, in range 0% - 100%
        """

        command = 10
        value = self.map(speed,0,100,0,127)
        self.write_message(self.address, command, value)

    def turn_left(self, speed: int):
        """
        Used to command vehicle to turn left in mixed mode. Valid data is 0-127; 0 = off, 127 = full speed.

        :param speed: the speed to set the motors, in range 0% - 100%
        """

        command = 11
        value = self.map(speed,0,100,0,127)
        self.write_message(self.address, command, value)

    def drive(self, speed: int):
        """
        Used to command vehicle forward or backward in mixed mode, at the cost of resolution
        of speed. Valid data is 0-127; 0 is full reverse, 64 is stop, and 127 is full forward.

        :param speed: the speed to set the motors, in range -100% to 100%
        """

        command = 12
        value = self.map(speed,-100,100,0,127)
        self.write_message(self.address, command, value)

    def turn(self, speed: int):
        """
        Used to command vehicle to turn right or left in mixed mode, at the cost of resolution
        of speed. Valid data is 0-127; 0 is full reverse, 64 is stop, and 127 is full forward.

        :param speed: the speed to set the motors, in range -100% to 100%
        """

        command = 13
        value = self.map(speed,-100,100,0,127)
        self.write_message(self.address, command, value)

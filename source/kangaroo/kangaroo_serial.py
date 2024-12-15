import time
import serial
import logging


class KangarooSerial:
    """
    Based on the Arduino library for the Kangaroo x2 Serial Backpack from
    Dimension Engineering. Deprecated.
    """
    KANGAROO_PORT = '/dev/ttyS0'

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

    def __init__(self):
        self.my_serial = serial.Serial(self.KANGAROO_PORT,
                                       timeout=0,
                                       baudrate=9600,
                                       parity=serial.PARITY_NONE,
                                       stopbits=serial.STOPBITS_ONE)



    def write(self, channel, command):
        if self.my_serial.is_open:
            command_to_send = channel + "," + command
            self.my_serial.write(command_to_send.encode())
            self.logger.debug(f"Sent {command_to_send} to IZZY.")
            time.sleep(0.1)
            if self.my_serial.in_waiting > 0:
                reply = self.my_serial.read(self.my_serial.in_waiting)
                self.logger.debug(f"Kangaroo returned: {reply}")
                return reply.decode()

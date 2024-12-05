# Kangaroo Serial Class
import serial
import logging


class KangarooSerial:
    KANGAROO_PORT = '/dev/ttyS0'

    def __init__(self):
        self.logger = logging.getLogger('KangarooSerial')
        logging.basicConfig(filename='kangarooSerial.log', level=logging.DEBUG)
        self.my_serial = serial.Serial(self.KANGAROO_PORT,
                                       timeout=0,
                                       baudrate=9600,
                                       parity=serial.PARITY_NONE,
                                       stopbits=serial.STOPBITS_ONE)

    def in_waiting(self):
        return self.my_serial.in_waiting

    def is_open(self):
        return self.my_serial.is_open

    def close(self):
        self.my_serial.close()

    def write(self, channel, command):
        if self.my_serial.is_open:
            command_to_send = channel.get_name() + "," + command
            self.logger.info('Sending serial command: ' + command_to_send +
                             " as " + command_to_send.encode)
            self.my_serial.write(command_to_send.encode())
            self.logger.info('Send complete.')
        else:
            self.logger.error('Error: port not open.')

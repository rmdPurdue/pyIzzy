import logging
from multimethod import multimethod


class KangarooChannel:
    def __init__(self, kangaroo_serial, name):
        self.logger = logging.getLogger('KangarooChannel')
        logging.basicConfig(filename='kangarooChannel.log', level=logging.DEBUG)
        self.kangaroo_serial = kangaroo_serial
        self.name = name

    def get_name(self):
        return self.name

    @multimethod
    def p(self, units: int):
        command = f'p{units} \r\n'
        self.kangaroo_serial.write(self.name, command)

    @multimethod
    def p(self, units: int, speed: int):
        command = f'p{units}s{speed} \r\n'
        self.kangaroo_serial.write(self.name, command)

    def s(self, units):
        command = f's{units}\r\n'
        self.kangaroo_serial.write(self.name, command)

    @multimethod
    def pi(self, units):
        command = f'pi{units}\r\n'
        self.kangaroo_serial.write(self.name, command)

    @multimethod
    def pi(self, units, speed):
        command = f'pi{units}s{speed}\r\n'
        self.kangaroo_serial.write(self.name, command)

    def si(self, units):
        command = f'si{units}\r\n'
        self.kangaroo_serial.write(self.name, command)

    def units(self, unit):
        command = f'units{unit}\r\n'
        self.kangaroo_serial.write(self.name, command)

    def get_s(self):
        command = 'gets\r\n'
        self.kangaroo_serial.write(self.name, command)

    def get_p(self):
        command = 'getp\r\n'
        self.kangaroo_serial.write(self.name, command)

    def start(self):
        command = 'start\r\n'
        self.kangaroo_serial.write(self.name, command)
        self.logger.info("System has started.\n")

    def power_down(self):
        command = 'powerdown\r\n'
        self.kangaroo_serial.write(self.name, command)
        self.logger.info("System has powered down.\n")

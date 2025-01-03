import logging
import multimethod


class KanagarooChannel():
    def __init__(self, kangaroo_serial, name):
        self.logger = logging.getLogger('KangarooChannel')
        logging.basicConfig(filename='kangarooChannel.log', level=logging.DEBUG)
        self.kangaroo_serial = kangaroo_serial
        self.name = name

    def get_name(self):
        return self.name

    @multimethod
    def p(self, units):
        command = ('p' + units + '\r' +'\n')
        self.kangaroo_serial.write(command)

    @multimethod
    def p(self, units, speed):
        command = ('p' + units + 's' + speed + '\r' +'\n')
        self.kangaroo_serial.write(command)

    def s(self, units):
        command = ('s' + units + '\r' +'\n')
        self.kangaroo_serial.write(command)

    @multimethod
    def pi(self, units):
        command = ('pi' + units + '\r' +'\n')
        self.kangaroo_serial.write(command)

    @multimethod
    def pi(self, units, speed):
        command = ('pi' + units + 's' + speed + '\r' +'\n')
        self.kangaroo_serial.write(command)

    def si(self, units):
        command = ('si' + units + '\r' +'\n')
        self.kangaroo_serial.write(command)

    def units(self, unit):
        command = ('units' + unit + '\r' +'\n')
        self.kangaroo_serial.write(command)

    def get_s(self):
        command = ('gets' + '\r' +'\n')
        self.kangaroo_serial.write(command)

    def get_p(self):
        command = ('getp' + '\r' +'\n')
        self.kangaroo_serial.write(command)

    def start(self):
        command = ('start' + '\r' +'\n')
        self.kangaroo_serial.write(command)
        self.logger.info("System has started.\n")

    def power_down(self):
        command = ('powerdown' + '\r' +'\n')
        self.kangaroo_serial.write(command)
        self.logger.info("System has powered down.\n")
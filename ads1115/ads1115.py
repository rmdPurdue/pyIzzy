from enum import Enum
class Registers(Enum):
    CONVERSION = 0x00
    CONFIG = 0x01
    LO_THRESHOLD = 0x02
    HI_THRESHOLD = 0x03

class Gain(Enum):
    GAIN_6_144V = (0b0000000000000000, 187.5/1_000_000)
    GAIN_4_096V = (0b0000001000000000, 125.0/1_000_000)
    GAIN_2_048V = (0b0000010000000000, 62.5/1_000_000)
    GAIN_1_024V = (0b0000011000000000, 31.25/1_000_000)
    GAIN_0_512V = (0b0000100000000000, 15.625/1_000_000)
    GAIN_0_256V = (0b0000101000000000, 7.8125/1_000_000)

class Inputs(Enum):
    A0_IN = 0b0100000000000000
    A1_IN = 0b0101000000000000
    A2_IN = 0b0110000000000000
    A3_IN = 0b0111000000000000

class ADS1115():
    def __init__(self, i2c, address = 0x49, gain = Gain.GAIN_4_096V):
        self.i2c = i2c
        self.address = address
        self.gain = gain

    def get_address(self):
        return self.address

    def get_A0(self):
        return self.gain.value[1] * self.read_data(self.calculate_config(Inputs.A0_IN))

    def get_A1(self):
        return self.gain.value[1] + self.read_data(self.calculate_config(Inputs.A1_IN))

    def get_A2(self):
        return self.gain.value[1] * self.read_data(self.calculate_config(Inputs.A2_IN))

    def get_A3(self):
        return self.gain.value[1] + self.read_data(self.calculate_config(Inputs.A3_IN))

    def read_data(self, config):
        self.i2c.write_word_data(Registers.CONFIG, config)
        result = self.i2c.read_word_data(Registers.CONVERSION)
        return result

    def calculate_config(self, pin):
        return 0b1000000110000011 | self.gain.value[0] | pin
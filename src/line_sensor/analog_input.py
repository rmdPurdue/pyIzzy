import ADS1x15


class AnalogIn:
    """
    A class for implementing analog reads for an ADS1115. Depends on the
    ADS1x15-ADC library from <http://github.com/chandrawi/ADS1x15-ADC>

    Attributes
    ----------
    ads: an ADS1115 object
        a specific ADS1115 instance whose pin we want to access

    pin: int
        the pin number of the pin for independent reads; valid pins 0-3

    Properties
    ----------
    value -> int
        the raw analog reading, between 0 and 65535 inclusive (16-bit). Read
        only.

    voltage -> float
        the analog reading converted to voltage. Read only.
    """

    def __init__(self, ads, pin):
        self._ads = ads
        self._pin = pin

    @property
    def reading(self) -> int:
        """Returns the value of the raw analog reading as a 16-bit int."""
        return self._ads.readADC(self._pin)

    @property
    def voltage(self) -> float:
        """Returns the voltage of the pin as a floating point value."""
        f = self._ads.toVoltage()
        return self.reading * f

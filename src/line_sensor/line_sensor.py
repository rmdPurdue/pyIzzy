class LineSensor:
    """
    A class that defines a line sensor for IZZY.

    Attributes
    ----------
        analog_in: analog_in object
            the object representing a physical input pin on an ADS1115

        slope: int
            the slope of readings [sensor offset / (max_reading - min_reading)]

    Properties
    ----------
        reading: int
            the current reading of the sensor (a 16-bit int)

        sensor_offset: int
            the distance (in mm) from IZZY center to sensor center

        min_reading: int
            the reading when the sensor is as far from the line as possible

        max_reading: int
            the reading when the sensor is as close to the line as possible

    Methods
    -------
        line_detected -> boolean
            returns true is the current reading is between the min and max
            reading values and false if it is not

        update_slope -> float
            updates the slope attribute with current values of sensor_offset,
            min_reading, and max_reading

    """

    _reading = 0

    def __init__(self,
                 analog_in,
                 offset: int = 23,
                 min_reading: int = 6000,
                 max_reading: int = 17000):
        self.analog_in = analog_in
        self._sensor_offset = offset
        self._min_reading = min_reading
        self._max_reading = max_reading
        self.slope = self.update_slope()

    @property
    def reading(self):
        """The current reading of the sensor (a 16-bit int)."""
        _reading = self.analog_in.reading
        return self._reading

    @property
    def sensor_offset(self):
        """The distance (in mm) from IZZY center to sensor center."""
        return self._sensor_offset

    @sensor_offset.setter
    def sensor_offset(self, offset: int):
        self._sensor_offset = offset
        self.slope = self.update_slope()

    @property
    def min_reading(self):
        """The reading when the sensor is as far from the line as possible."""
        return self._min_reading

    @min_reading.setter
    def min_reading(self, reading: int):
        self._min_reading = reading
        self.slope = self.update_slope()

    @property
    def max_reading(self):
        """The reading when the sensor is as close to the line as possible."""
        return self._max_reading

    @max_reading.setter
    def max_reading(self, reading: int):
        self._max_reading = reading
        self.slope = self.update_slope()

    def line_detected(self):
        return self._max_reading > self.reading > self._min_reading

    def update_slope(self):
        return self.sensor_offset / (self._max_reading - self._min_reading)

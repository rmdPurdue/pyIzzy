class SensorArray:
    """
    A class to define an array of analog sensors.

    Attributes
    ----------
        sensors: list
            a list containing individual analog_in objects.

        y_offset: int
            the offset front-to-back of the sensor array from the center of
            IZZY.

    Methods
    -------
        line_detected -> boolean
            polls the sensors to see if they have detected the line; ORs the
            boolean values together and returns the subsequent value.

        x_error -> float
            calculates the offset from the line: the sum of the
            reading of each sensor multiplied by its slope (x-offst over the
            average reading). Sensors to the left of center contribute negative
            offset; those to the right contribute positive. For an odd-number
            of sensors. the center sensor contributes to whichever offset (
            negative or positive) has a larger magnitude.
    """

    def __init__(self, y_offset: int, *sensors):
        self.sensors = sensors
        self.y_offset = y_offset

    def line_detected(self):
        """
        Polls the sensors to see if they have detected the line.

        :return: boolean
        """

        detected = False
        for sensor in self.sensors:
            detected |= sensor.line_detected()
        return detected

    def x_error(self) -> float:
        """
        Calculates the offset from the line.

        :return: float
        """

        neg_error = 0
        pos_error = 0
        sensor_count = len(self.sensors)
        if sensor_count % 2 == 0:
            for sensor in self.sensors[0: sensor_count // 2 - 1]:
                neg_error += sensor.reading * sensor.slope
            for sensor in self.sensors[sensor_count // 2: sensor_count - 1]:
                pos_error += sensor.reading * sensor.slope
        else:
            for sensor in self.sensors[0: sensor_count // 2 - 1]:
                neg_error += sensor.reading * sensor.slope
            for sensor in self.sensors[sensor_count // 2 + 1: sensor_count - 1]:
                pos_error += sensor.reading * sensor.slope
            if neg_error >= pos_error:
                neg_error += (self.sensors[sensor_count // 2].reading *
                              self.sensors[sensor_count // 2].slope)
            else:
                pos_error += (self.sensors[sensor_count // 2].reading *
                              self.sensors[sensor_count // 2].slope)
        return pos_error - neg_error

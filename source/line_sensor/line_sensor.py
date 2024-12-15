class LineSensor:
    SENSOR_OFFSET = 2.3  # Distance (in cm) from IZZY center to the middle of sensor
    min_reading = 6000
    max_reading = 17000
    reading = 0
    slope = 0

    def __init__(self, threshold, pin, name, ads1115):
        self.threshold = threshold
        self.pin = pin
        self.name = name
        self.ads1115 = ads1115
        self.update_slope()

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_reading(self):
        if self.pin == 0:
            self.reading = self.ads1115.get_a0()
        elif self.pin == 1:
            self.reading = self.ads1115.get_a1()
        elif self.pin == 2:
            self.reading = self.ads1115.get_a2()
        elif self.pin == 3:
            self.reading = self.ads1115.get_a3()
        return self.reading * 10000

    def get_state(self):
        return self.reading < self.get_threshold()

    def get_name(self):
        return self.name

    def get_max_reading(self):
        return self.max_reading

    def get_min_reading(self):
        return self.min_reading

    def set_min_reading(self, min_reading):
        self.min_reading = min_reading

    def set_max_reading(self, max_reading):
        self.max_reading = max_reading

    def get_slope(self):
        return self.slope

    def update_slope(self):
        self.slope = self.SENSOR_OFFSET / (self.max_reading - self.min_reading)

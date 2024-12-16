import math


class PID:
    """
    Calculates the error using a PID loop.

    Attributes
    ----------
        kp: float
            proportional gain coefficient

        ki: float
            integral gain coefficient

        kd: float
            derivative gain coefficient

    Properties
    ----------
        pid_value: float
            the sum of the proportional, integral, and derivative errors

        error: float
            the magnitude of the current error

        total_error: float
            the running sum of errors

        previous_error: float
            the magnitude of the previous error calculation

        Methods
        -------
        calculate_pid -> float
            returns the PID correction value

        get_error_angle -> float
            returns the angle of offset from the line based on the PID
            correction value and the y-offset of the sensor array from the
            center of the platform

        reset:
            resets error, total_error, previous_error, and pid_value to zero
            and sets the proportional, integral, and derivative gain
            coefficients to default values.
    """

    _pid_value = 0
    _error = 0
    _total_error = 0
    _previous_error = 0

    def __init__(self, sensors, kp=1, ki=0, kd=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.sensors = sensors

    @property
    def pid_value(self):
        return self._pid_value

    @property
    def error(self):
        return self._error

    @property
    def total_error(self):
        return self._total_error

    @property
    def previous_error(self):
        return self._previous_error

    def calculate_pid(self):
        self._error = self.sensors.x_error()
        proportional = self.kp * self._error
        integral = self.ki * self._total_error
        derivative = self.kd * (self._error - self._previous_error)
        self._pid_value = proportional + integral + derivative
        self._total_error += self.error
        self._previous_error = self.error
        return self.pid_value

    def get_error_angle(self):
        return (-((math.atan(self._pid_value / self.sensors.y_offset)) * 180) /
                math.pi)

    def reset(self):
        self._error = 0
        self._total_error = 0
        self._previous_error = 0
        self.kp = 1
        self.ki = 0
        self.kd = 0
        self._pid_value = 0

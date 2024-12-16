# Based on ObstacleAvoidance.py by Kevin Simonson
# originally coded 05/03/2023
from rplidar import RPLidar
import time
import numpy
from src.movement.drive_movement import DriveMovement


class ObstacleResponder(DriveMovement):
    RPLIDAR_PORT = '/dev/ttyUSB0'
    return_left = False
    return_right = False
    scan_angles = list()
    scan_distances = list()
    average_angle = 0
    average_distance = 0

    def __init__(self, port_name = RPLIDAR_PORT, stop_threshold=500, avoid_threshold=1000,left_limit=45,right_limit=315,
                 averaging_interval=2, x=0, y=0, z=0):
        super().__init__(x, y, z)
        self.port_name = port_name
        self.stop_threshold = stop_threshold
        self.avoid_threshold = avoid_threshold
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.averaging_interval = averaging_interval
        self.lidar = RPLidar(port_name)

    def set_stop_threshold(self, stop_threshold):
        self.stop_threshold = stop_threshold

    def set_avoid_threshold(self, avoid_threshold):
        self.avoid_threshold = avoid_threshold

    def set_avoidance_angle_limits(self, left, right):
        self.left_limit = left
        self.right_limit = right

    def set_averaging_interval(self, interval):
        self.averaging_interval = interval

    def stop_avoiding(self):
        self.lidar.stop_motor()

    def avg(self, values):
        avg_value = numpy.mean(values)

        values.clear()

        return avg_value

    def start_avoiding(self):
        self.lidar.start_motor()
        time.sleep(2)

        start_time = time.time()

        for scan in self.lidar.iter_scans():
            for quality, angle, distance in scan:
                if distance < self.stop_threshold and (angle > self.left_limit or angle < self.right_limit):
                    # stop: cannot avoid
                    pass
                elif distance < self.avoid_threshold and (angle > self.left_limit or angle < self.right_limit):
                    #add angle, distance to lists of scanned values
                    self.scan_angles.append(angle)
                    self.scan_distances.append(distance)

                    # check the time interval
                    if time.time() - start_time >= self.averaging_interval:
                        # average the scanned values
                        self.average_angle = self.avg(self.scan_angles)
                        self.average_distance = self.avg(self.scan_distances)

                        # reset time
                        start_time = time.time()

                    if angle < self.right_limit:
                        # Object on right side at avg angle and avg distance

                        if not self.return_right:
                            self.turn(self.average_angle - 90, self.current_speed / 2)

                            self.right_limit = 100
                            self.return_right = True
                        else:
                            self.turn(90 - self.average_angle, self.current_speed / 2)
                            pass

                        #elif line detected?
                    elif angle > self.left_limit:
                        #object on left side at avg angle and avg distance
                        if not self.return_left:
                            self.turn(self.average_angle - 360 + 90, self.current_speed / 2)

                            self.left_limit = 260
                            self.return_left = True
                        else:
                            self.turn(-90 - self.average_angle - 360, self.current_speed / 2)
                            pass

                        #elif line detected?
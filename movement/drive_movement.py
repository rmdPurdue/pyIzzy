import math

class IzzyMovement():
    def __init__(self, x = 0, y = 0, z = 0):
        self.home = {"x": x, "y": y, "z": z}
        self.position = {"x": x, "y": y, "z": z}
        self.angle = 0

    def setup(self, wheel_radius, system_radius, lines_per_rotation):
        self.wheel_radius = wheel_radius
        self.system_radius = system_radius
        self.lines_per_rotation = lines_per_rotation

    def set_channels(self, drive_channel, turn_channel):
        self.drive_channel = drive_channel
        self.turn_channel = turn_channel
        self.drive_channel.start()
        self.turn_channel.start()
        self.drive_channel.units("1 rotation = 512 lines")

    def get_drive_position(self):
        return self.drive_channel.getP()

    def get_drive_speed(self):
        return self.drive_channel.getS()

    def get_coordinates(self):
        return self.position

    def get_angle(self):
        return self.angle

    def update_coordinates(self, coords):
        self.position = coords

    def update_angle(self, angle):
        self.angle = angle

    def turn(self, target_angle):
        angle = self.system_radius * 360 * self.lines_per_rotation
        if target_angle == 0: angle = 0
        else: angle = angle / (target_angle * self.wheel_radius)
        self.turn_channel.P(angle)

    def move(self, distance, speed = 10):
        self.drive_channel.P(distance)
        self.drive_channel.S(speed)

    def simple_move(self, target_position, angle_direction):
        if self.position["x"] == target_position["x"] and self.position["y"] != target_position["y"]:
            cw_angle = 90
            ccw_angle = 270
        else:
            tan_angle = math.tan(self.position["y"] / (self.position["x"] * 360 / (2 * math.pi)))
            if target_position["x"] > self.position["x"]:
                if target_position["y"] > self.position["y"]:
                    ccw_angle = tan_angle
                    cw_angle = 360 - tan_angle
                else:
                    ccw_angle = 360 - tan_angle
                    cw_angle = tan_angle
            else:
                if target_position["y"] > self.position["y"]:
                    ccw_angle = 180 - tan_angle
                    cw_angle = 180 + tan_angle
                else:
                    ccw_angle = 180 + tan_angle
                    cw_angle = 180 - tan_angle
        if angle_direction == 1:
            self.turn(-cw_angle)
        elif angle_direction == -1:
            self.turn(ccw_angle)
        else:
            if abs(self.angle - ccw_angle) > abs(self.angle - cw_angle):
                self.turn(-cw_angle)
            else:
                self.turn(ccw_angle)
        distance = math.sqrt(pow(self.position["x"], 2) + pow(self.position["y"], 2))
        self.move(distance)
        self.update_coordinates(target_position)
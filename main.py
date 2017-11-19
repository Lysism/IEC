import math

SAT_SPEED = 100
SPEED_OF_WAVE = 350
EPSILON = 0.1

def deg2rad(deg):
    return deg * math.pi / 180

def rad2deg(rad):
    return rad * 180 / math.pi

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def intersections(self, other):
        dist = self.distance(other)
        if dist > (self.r + other.r):
            # no intersections, circles are too far apart
            return []
        elif dist < abs(self.r - other.r):
            # no intersections, one circle contains another
            return []
        elif 

if __name__ == "__main__":
    # swap sin and cos all the time for weird coords
    with open("sample_input_3.txt") as f:
        text = f.readlines()
    num_sats, recv_time, dest_x, dest_y = map(float, text[0].split(' '))

    destination = Point(dest_x, dest_y)

    sats = []
    for line in text[1:]:
        initial_x, initial_y, heading, send_time = map(float, line.split(' '))

        send_x = initial_x + math.sin(deg2rad(heading)) * SAT_SPEED * send_time
        send_y = initial_y + math.cos(deg2rad(heading)) * SAT_SPEED * send_time

        sat_pos = Point(send_x, send_y)

        plane_distance_from_sat = (recv_time - send_time) * SPEED_OF_WAVE

        sats.append((sat_pos, plane_distance_from_sat))

    # list of ((x, y), distance from airplane)
    print(sats)
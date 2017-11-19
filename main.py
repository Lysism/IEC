import math
import matplotlib.pyplot as plt
from itertools import combinations

SAT_SPEED = 100
SPEED_OF_WAVE = 350
EPSILON = 0.1

def inconclusive():
    print("Inconclusive")
    exit(1)

def deg2rad(deg):
    return deg * math.pi / 180

def rad2deg(rad):
    return rad * 180 / math.pi

def flip_rad(rad):
    x = math.cos(rad)
    y = math.sin(rad)
    #flip coords
    return math.atan2(x, y)

def flip_deg(deg):
    return rad2deg(flip_rad(deg2rad(deg)))

def normalize_deg(deg):
    while deg < 0:
        deg += 360
    while deg > 360:
        deg -= 360
    return deg
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def average(points):
        avg_x = sum(point.x for point in points) / len(points)
        avg_y = sum(point.y for point in points) / len(points)
        return Point(avg_x, avg_y)

    def __repr__(self):
        return str("Point({}, {})".format(self.x, self.y))

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def __str__(self):
        return "{}, {}".format(self.x, self.y)


class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __str__(self):
        return "x:{}, y:{}, r:{}".format(self.x, self.y, self.r)

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    # algorithm for circle intersections
    # modified from http://paulbourke.net/geometry/circlesphere/circle_intersection.py
    def intersect(self, other):
        PREC = 2
        dist = round(self.distance(other), PREC)
        dx = other.x - self.x
        dy = other.y - self.y
        if dist > (self.r + other.r):
            # no intersections, circles are too far apart
            return []
        elif dist < abs(self.r - other.r):
            # no intersections, one circle contains another
            return []

        elif dist == 0 and self.r == other.r:
            # circles are the same, infinite solutions
            return []
        else:
            chord_dist = (self.r ** 2 - other.r ** 2 + dist ** 2) / (2 * dist)
            half_chord = math.sqrt(self.r ** 2 - chord_dist ** 2)

            chord_mid_x = self.x + (chord_dist * dx) / dist
            chord_mid_y = self.y + (chord_dist * dy) / dist

            int_1_x = round(chord_mid_x + (half_chord * dy) / dist, PREC)
            int_1_y = round(chord_mid_y - (half_chord * dx) / dist, PREC)
            int_2_x = round(chord_mid_x - (half_chord * dy) / dist, PREC)
            int_2_y = round(chord_mid_y + (half_chord * dx) / dist, PREC)
            return [Point(int_1_x, int_1_y), Point(int_2_x, int_2_y)]


if __name__ == "__main__":
    fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
    ax.set_xbound(-1100, 1100)
    ax.set_ybound(-1100, 1100)
    plt.grid(True)
    ax.set_aspect('equal', 'datalim')
    # swap sin and cos all the time for weird coords
    with open("synthetic_input_1.txt") as f:
        text = f.readlines()

    num_sats, recv_time, dest_x, dest_y = map(float, text[0].split(' '))
    if num_sats < 3:
        inconclusive()
    destination = Point(dest_x, dest_y)

    sats = []
    for line in text[1:]:
        initial_x, initial_y, heading, send_time = map(float, line.split(' '))

        # location of satellite when it sent the signal

        send_x = initial_x + math.sin(deg2rad(heading)) * SAT_SPEED * send_time
        send_y = initial_y + math.cos(deg2rad(heading)) * SAT_SPEED * send_time

        sat_pos = Point(send_x, send_y)

        plane_distance_from_sat = (recv_time - send_time) * SPEED_OF_WAVE

        sats.append(Circle(send_x, send_y, plane_distance_from_sat))

        ax.add_artist(plt.Circle((send_x, send_y), plane_distance_from_sat, edgecolor='blue', alpha=0.1))
        plt.plot([send_x], [send_y], marker='o', markersize=3, color='black')
    all_intersections = []
    for a,b in combinations(sats, 2):
        all_intersections.extend(a.intersect(b))
    
    ranked_intersections = []
    for point in all_intersections:
        plt.plot(point.x, point.y, marker='o', markersize=2, color='green')            
        count = 0
        for other in all_intersections:
            if point.distance(other) < EPSILON:
                count += 1
        ranked_intersections.append((count, point))

    ## sort by number of nearby intersections, ranked high -> low
    sorted_ranks = sorted(ranked_intersections, key=lambda x: x[0], reverse=True)
    max_intersections = sorted_ranks[0][0]
    good_intersections = [tup[1] for tup in sorted_ranks if tup[0] == max_intersections]
    
    ## make sure data is consistant and interseactions are nearby
    for a, b in combinations(good_intersections, 2):
        if a.distance(b) > EPSILON:
            print("Inconsistent")
            exit(1)
    airplane = Point.average(good_intersections)
    dx = destination.x - airplane.x
    dy = destination.y - airplane.y
    rad_to_plane = math.atan2(dy, dx)
    print(normalize_deg(rad2deg(flip_rad(rad_to_plane))))
    plt.plot([airplane.x], [airplane.y], marker='o', markersize=5, color='red')    
    plt.plot([destination.x], [destination.y], marker='o', markersize=5, color='blue')    
    print(str(airplane))
    plt.plot([airplane.x, destination.x], [airplane.y, destination.y], color='orange', alpha=0.5)    
    Ad = airplane.distance(destination)
    Ax = [airplane.x, airplane.x+Ad*math.cos(rad_to_plane)]
    Ay = [airplane.y, airplane.y+Ad*math.sin(rad_to_plane)]
    plt.plot(Ax, Ay, '-')
    plt.show()
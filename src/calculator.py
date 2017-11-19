import math
import time
from itertools import combinations

SAT_SPEED = 100
SPEED_OF_WAVE = 350
EPSILON = 0.1


def deg2rad(deg):
    """
    A function to convert degrees into radians
    Running time: O(1)
    :param deg: The value to convert
    :return: The converted value
    """
    return deg * math.pi / 180


def rad2deg(rad):
    """
    A function to convert radians into degrees
    Running time: O(1)
    :param rad: The value to convert
    :return: The converted value
    """
    return rad * 180 / math.pi


def flip_rad(rad):
    """
    Flips the x and y coordinates using cosine and sine functions
    Running time: O(1)
    :param rad: The radians value to use with consine and sine functions
    :return: The arctan value of x and y
    """
    x = math.cos(rad)
    y = math.sin(rad)
    # Pass the coordinates backwards into atan2
    # so we swap X and Y
    return math.atan2(x, y)


def flip_deg(deg):
    """
    Flips the degree values
    Running time: O(1)
    :param deg: The degree value to flip using function calls
    :return: The flipped value
    """
    return rad2deg(flip_rad(deg2rad(deg)))


def normalize_deg(deg):
    """
    Normalizes angle orientations for the given degree value
    Running time: O(1)
    :param deg: The value to normalize
    :return: The normalized value
    """
    while deg < 0:
        deg += 360
    while deg > 360:
        deg -= 360
    return deg


class Point(object):
    def __init__(self, x, y):
        """
        Constructor for the Point class
        Running time: O(1)
        :param x: The x coordinate value
        :param y: The y coordinate value
        """
        self.x = x
        self.y = y

    @staticmethod
    def average(points):
        """
        Averages the x and y coordinate values from all given points
        Running time: O(1)
        :return: The average x value and average y value
        """
        avg_x = sum(point.x for point in points) / len(points)
        avg_y = sum(point.y for point in points) / len(points)
        return Point(avg_x, avg_y)

    def __repr__(self):
        """
        Returns a string representation of a Point object
        Running time: O(1)
        :return: String containing the point's coordinates formatted
        """
        return str("Point({}, {})".format(self.x, self.y))

    def distance(self, other):
        """
        Calculates Euclidean distance between two given points
        Running time: O(1)
        :param other: The second point to calculate distance with the first point
        :return: The distance value calculated
        """
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def __str__(self):
        """
        Returns a formatted string with the coordinates
        Running time: O(1)
        :return: The formatted string
        """
        return "{}, {}".format(self.x, self.y)


class Circle(object):
    def __init__(self, x, y, r):
        """
        Constructor for the Circle class
        Running time: O(1)
        :param x: The x coordinate value
        :param y: The y coordinate value
        :param r: The radius value
        """
        self.x = x
        self.y = y
        self.r = r

    def __str__(self):
        """
        Returns a string representation of the object
        Running time: O(1)
        :return: Formatted string with the object's parameters
        """
        return "x:{}, y:{}, r:{}".format(self.x, self.y, self.r)

    def distance(self, other):
        """
        Calculates Euclidean between the two given points
        Running time: O(1)
        :param other: The second point to use in calculations with the first point
        :return: The calculated distance value
        """
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    # algorithm for circle intersections
    # modified from http://paulbourke.net/geometry/circlesphere/circle_intersection.py
    def intersect(self, other):
        """
        Check for intersections with signal circles radiating from satellite points
        Running time: O(1)
        :param other: The second satellite point
        :return: The intersection points of the two circles
        """
        dist = self.distance(other)
        dx = other.x - self.x
        dy = other.y - self.y
        if dist > (self.r + other.r):
            # no intersections, circles are too far apart
            return []
        if dist < abs(self.r - other.r):
            # no intersections, one circle contains another
            return []

        if dist == 0 and self.r == other.r:
            # circles are the same, infinite solutions
            return []
        chord_dist = (self.r ** 2 - other.r ** 2 + dist ** 2) / (2 * dist)
        half_chord = math.sqrt(self.r ** 2 - chord_dist ** 2)

        chord_mid_x = self.x + (chord_dist * dx) / dist
        chord_mid_y = self.y + (chord_dist * dy) / dist

        int_1_x = chord_mid_x + (half_chord * dy) / dist
        int_1_y = chord_mid_y - (half_chord * dx) / dist
        int_2_x = chord_mid_x - (half_chord * dy) / dist
        int_2_y = chord_mid_y + (half_chord * dx) / dist
        return [Point(int_1_x, int_1_y), Point(int_2_x, int_2_y)]


def calculate_positions(text):
    """
    Calculates the positions of the satellites moving from the given time and coordinates
    Calculates the location of the plane from the best intersection point of the
    satellite signals. Calculates the bearing for the plane to its destination point.
    Running time: O(n^2)
    :param text: The input values from the text files
    :return: The final values for all positions (satellites, plane, and destination), intersections, and the bearing all in a dictionary
    """
    num_sats, recv_time, dest_x, dest_y = map(float, text[0].split(' '))
    if num_sats < 3:
        return {"err": "Inconclusive"}
    destination = Point(dest_x, dest_y)

    sats = []
    for line in text[1:]:
        initial_x, initial_y, heading, send_time = map(float, line.split(' '))

        # location of satellite when it sent the signal
        send_x = initial_x + math.sin(deg2rad(heading)) * SAT_SPEED * send_time
        send_y = initial_y + math.cos(deg2rad(heading)) * SAT_SPEED * send_time

        plane_distance_from_sat = (recv_time - send_time) * SPEED_OF_WAVE

        sats.append(Circle(send_x, send_y, plane_distance_from_sat))

    all_intersections = []
    for a, b in combinations(sats, 2):
        all_intersections.extend(a.intersect(b))

    ranked_intersections = []
    for point in all_intersections:
        count = 0
        for other in all_intersections:
            if point.distance(other) < EPSILON:
                count += 1
        ranked_intersections.append((count, point))
    # sort by number of nearby intersections, ranked high -> low
    sorted_ranks = sorted(ranked_intersections,
                          key=lambda x: x[0], reverse=True)
    max_intersections = sorted_ranks[0][0]
    good_intersections = [tup[1]
                          for tup in sorted_ranks if tup[0] == max_intersections]

    # make sure data is consistant and interseactions are nearby
    for a, b in combinations(good_intersections, 2):
        if a.distance(b) > EPSILON:
            return {"error": "Inconsistent"}

    airplane = Point.average(good_intersections)
    dx = destination.x - airplane.x
    dy = destination.y - airplane.y
    rad_to_plane = math.atan2(dy, dx)
    deg_to_plane = normalize_deg(rad2deg(flip_rad(rad_to_plane)))
    return {
        "deg": deg_to_plane,
        "rad": rad_to_plane,
        "plane": {
            "x": airplane.x,
            "y": airplane.y,
            "v": 100
        },
        "dest": {
            "x": destination.x,
            "y": destination.y,
            "v": 100
        },
        "sats": [{"x": sat.x, "y": sat.y, "z": sat.r} for sat in sats],
        "all_intersections": [{"x": point.x, "y": point.y, "z": 100} for point in all_intersections],
        "good_intersections": [{"x": point.x, "y": point.y, "z": 100} for point in good_intersections]
    }


def debug_plot(data):
    """
    Plots the data using matplotlib and outputs the data in a plot
    Running time: O(n)
    :param data: The data input generated from calculate_positions()
    :return: None
    """
    import matplotlib.pyplot as plt
    _, axes = plt.subplots()
    axes.set_xbound(-1100, 1100)
    axes.set_ybound(-1100, 1100)
    plt.grid(True)
    axes.set_aspect('equal', 'datalim')
    for sat in data["sats"]:
        axes.add_artist(plt.Circle(
            (sat["x"], sat["y"]), sat["z"], edgecolor='blue', alpha=0.1))
        plt.plot(sat["x"], sat["y"], marker='o', markersize=3, color='black')

    for point in data["all_intersections"]:
        plt.plot(point["x"], point["y"], marker='o',
                 markersize=1, color='green')

    for point in data["good_intersections"]:
        plt.plot(point["x"], point["y"], marker='o',
                 markersize=3, color='yellow')

    plane = data["plane"]
    destination = data["dest"]

    plt.plot([plane["x"]], [plane["y"]],
             marker='o', markersize=5, color='red')
    plt.plot([destination["x"]], [destination["y"]],
             marker='o', markersize=5, color='blue')
    plt.plot([plane["x"], destination["x"]], [plane["y"],
                                              destination["y"]], color='orange', alpha=0.5)
    plt.show()


if __name__ == "__main__":
    # swap sin and cos all the time for weird coords
    start_time = time.clock()
    with open("sample_input_3.txt") as f:
        LINES = f.readlines()

    OUTPUT = calculate_positions(LINES)
    #Calculate the running time of the program (not including time spent on viewing plot)
    end_time = time.clock()
    print ("Running time: " + str(end_time - start_time) + " seconds")
    print(OUTPUT["deg"])
    debug_plot(OUTPUT)

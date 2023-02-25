import os.path
from tkinter import *


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Point:
    x: float
    y: float
    x_var: DoubleVar
    y_var: DoubleVar
    visible: bool

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.x_var = DoubleVar()
        self.x_var.set(self.x)
        self.y_var = DoubleVar()
        self.y_var.set(self.y)

    def __str__(self):
        return "[" + str(self.x) + ";" + str(self.y) + "]"

    def round(self, precision):
        self.x = round(self.x, precision)
        self.y = round(self.y, precision)
        return self

    def update_vars(self):
        self.x_var.set(self.x)
        self.y_var.set(self.y)

    def print(self):
        print("{: ^ 10.3f}|{: ^ 10.3f}".format(self.x, self.y))


class PointTable:
    """ From CA lab 01 """
    epsilon = 1e-6
    function = 'y'
    argument = 'x'
    points: list[Point]

    def from_points(self, points: list[Point]) -> None:
        self.points = points

    def from_file(self, file_name: str) -> None:
        with open(file_name, 'r') as file:
            line = file.readline()
            line = line.rstrip()
            item = line.split(" ")
            try:
                float(item[0])
            except ValueError:
                self.argument = item[0]
                self.function = item[1]
                line = file.readline()
                line = line.rstrip()
                item = line.split(" ")
            value_amount = len(item)

        if not os.path.isfile(file_name):
            print("No such file:", file_name)
            raise IOError

        self.points: list[Point] = []
        with open(file_name, 'r') as file:
            for i, line in enumerate(file):
                line = line.rstrip()
                item = line.split(" ")
                try:
                    float(item[0])
                except ValueError:
                    if i != 0:
                        raise ValueError
                    continue

                if len(item) != value_amount:
                    print("Incorrect amount of values in line:", line, "expected", value_amount, "values")
                    raise ValueError
                derivatives = []
                try:
                    x, y = map(float, item[:2])
                    if len(item) > 2:
                        derivatives = list(map(float, item[2:]))
                except ValueError:
                    print("File contains corrupted line:", line)
                    raise ValueError
                point = Point(x, y)
                self.points.append(point)
        self.points.sort(key=lambda e: e.x)

    def __len__(self):
        return len(self.points)

import math

import itertools

import numpy as np

from functions import to_radians, multiply_matrices

from copy import deepcopy


class FloatVector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class IntVector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Point:
    x: float
    y: float
    extra: float
    visible: bool

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.extra = 1

    def __str__(self):
        return "[{:.6g};{:.6g}]".format(self.x, self.y)

    def round(self, precision):
        self.x = round(self.x, precision)
        self.y = round(self.y, precision)
        return self

    def print(self):
        print("{: ^ 10.3f}|{: ^ 10.3f}".format(self.x, self.y))

    def move(self, diff_x: float, diff_y: float):
        self.x += diff_x
        self.y += diff_y

    def move_to(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    start: Point
    end: Point
    points: list[Point]

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.points = list([start, end])

    def move_to(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.points = list([start, end])


class Circle:
    center: Point
    points: list[Point]
    radius: float

    def __init__(self, center_x: float, center_y: float, radius: float):
        self.points = list()
        self.radius = radius
        self.center = Point(center_x, center_y)
        self.set_points()

    def set_points(self):
        self.points.clear()

        angle = 0
        while angle < 2 * math.pi:
            x = self.center.x + self.radius * math.sin(angle)
            y = self.center.y + self.radius * math.cos(angle)
            self.points.append(Point(x, y))
            angle += 1 / self.radius

    def move(self, diff_x: float, diff_y: float):
        for point in self.points:
            point.x += diff_x
            point.y += diff_y


class Astroid:
    center: Point
    points: list[Point]
    radius: float

    def __init__(self, center_x: float, center_y: float, radius: float):
        self.points = list()
        self.radius = radius
        self.center = Point(center_x, center_y)
        self.set_points()

    def set_points(self):
        self.points.clear()

        angle = 0
        while angle < 2 * math.pi:
            x = self.center.x + self.radius * math.cos(angle) ** 3
            y = self.center.y + self.radius * math.sin(angle) ** 3
            self.points.append(Point(x, y))
            angle += 1 / self.radius

    def move(self, diff_x: float, diff_y: float):
        for point in self.points:
            point.x += diff_x
            point.y += diff_y


class LineList(list):
    def __init__(self, lines: list[Line]):
        super().__init__()
        self.extend(lines)

    def get_points(self):
        points = [point for line in self for point in line.points]
        return itertools.chain(set(point for point in points))


class Figure:
    astroid: Astroid
    circle: Circle
    lines: LineList[Line]
    history_prev: list
    history_next: list

    def __init__(self, center_x: float, center_y: float, radius: float):
        self.center = Point(center_x, center_y)
        self.radius = radius

        self.astroid = Astroid(center_x, center_y, radius)
        self.circle = Circle(center_x, center_y, radius / 3)

        left_top_point, left_bottom_point,\
            right_top_point, right_bottom_point = self.get_corner_points()

        self.left_line = Line(left_top_point, left_bottom_point)
        self.bottom_line = Line(left_bottom_point, right_bottom_point)
        self.right_line = Line(right_top_point, right_bottom_point)

        self.lines = LineList([self.left_line, self.bottom_line, self.right_line])

        self.history_prev = list()
        self.history_next = list()

    def get_corner_points(self):
        left_top_point = Point(self.center.x - self.radius, self.center.y)
        left_bottom_point = Point(self.center.x - self.radius, self.center.y - self.radius * 2)
        right_top_point = Point(self.center.x + self.radius, self.center.y)
        right_bottom_point = Point(self.center.x + self.radius, self.center.y - self.radius * 2)

        return left_top_point, left_bottom_point, right_top_point, right_bottom_point

    def get_points(self):
        return itertools.chain(self.astroid.points, self.circle.points, self.lines.get_points(), [self.center])

    def get_drawable_points(self):
        return itertools.chain(self.astroid.points, self.circle.points)

    def get_lines(self):
        return self.lines

    def move_to_center(self, center_x: float, center_y: float):
        diff_x = center_x - self.center.x
        diff_y = center_y - self.center.y
        self.move(diff_x, diff_y)

        self.center.x = center_x
        self.center.y = center_y

    def move(self, diff_x: float, diff_y: float):
        self.write_history()

        # points = self.get_points()
        # for point in points:
        #     point.move(diff_x, diff_y)

        move_matrix = np.array([[1, 0, diff_x], [0, 1,  diff_y], [0, 0, 1]])

        points = self.get_points()
        for point in points:
            self.apply_transformation_matrix(point, move_matrix)

    def scale(self, center: FloatVector, scale: FloatVector):
        self.write_history()

        # points = self.get_points()
        # for point in points:
        #     new_x = float(center.x + (point.x - center.x) * scale.x)
        #     new_y = float(center.y + (point.y - center.y) * scale.y)
        #     point.move_to(new_x, new_y)

        center.x *= -1
        center.y *= -1

        move_to_global = np.array([[1, 0, -center.x], [0, 1, -center.y], [0, 0, 1]])
        scale_matrix = np.array([[scale.x, 0, 0], [0, scale.y, 0], [0, 0, 1]])
        move_to_local = np.array([[1, 0, center.x], [0, 1,  center.y], [0, 0, 1]])

        transformation_matrix = multiply_matrices(move_to_global, scale_matrix)
        transformation_matrix = multiply_matrices(transformation_matrix, move_to_local)

        points = self.get_points()
        for point in points:
            self.apply_transformation_matrix(point, transformation_matrix)

    def rotate(self, center: FloatVector, angle_degrees: float):
        self.write_history()

        # sin_a = math.sin(to_radians(angle_degrees))
        # cos_a = math.cos(to_radians(angle_degrees))
        #
        # points = self.get_points()
        # for point in points:
        #     rotation_x = point.x - center.x
        #     rotation_y = point.y - center.y
        #     new_x = float(center.x + rotation_x * cos_a - rotation_y * sin_a)
        #     new_y = float(center.y + rotation_y * cos_a + rotation_x * sin_a)
        #     point.move_to(new_x, new_y)

        center.x *= -1
        center.y *= -1

        sin_a = math.sin(to_radians(angle_degrees))
        cos_a = math.cos(to_radians(angle_degrees))

        move_to_global = np.array([[1, 0, -center.x], [0, 1, -center.y], [0, 0, 1]])
        rotate_matrix = np.array([[cos_a, -sin_a, 0], [sin_a, cos_a, 0], [0, 0, 1]])
        move_to_local = np.array([[1, 0, center.x], [0, 1,  center.y], [0, 0, 1]])

        transformation_matrix = multiply_matrices(move_to_global, rotate_matrix)
        transformation_matrix = multiply_matrices(transformation_matrix, move_to_local)

        points = self.get_points()
        for point in points:
            self.apply_transformation_matrix(point, transformation_matrix)

    def write_page(self):
        return list([deepcopy(self.astroid), deepcopy(self.circle), deepcopy(self.lines), deepcopy(self.center)])

    def write_history(self):
        self.history_next.clear()
        new_page = list([deepcopy(self.astroid), deepcopy(self.circle), deepcopy(self.lines), deepcopy(self.center)])
        self.history_prev.append(new_page)

    def undo(self):
        curr_page = self.write_page()
        prev_page = self.history_prev[-1]
        self.astroid = prev_page[0]
        self.circle = prev_page[1]
        self.lines = prev_page[2]
        self.center = prev_page[3]
        self.history_next = [curr_page] + self.history_next
        self.history_prev = self.history_prev[:-1]

    def redo(self):
        curr_page = self.write_page()
        prev_page = self.history_next[0]
        self.astroid = prev_page[0]
        self.circle = prev_page[1]
        self.lines = prev_page[2]
        self.center = prev_page[3]
        self.history_prev.append(curr_page)
        self.history_next = self.history_next[1:]

    @staticmethod
    def apply_transformation_matrix(point: Point, matrix: np.ndarray):
        new_x = point.x * matrix[0][0] + point.y * matrix[0][1] + point.extra * matrix[0][2]
        new_y = point.x * matrix[1][0] + point.y * matrix[1][1] + point.extra * matrix[1][2]
        new_extra = point.x * matrix[2][0] + point.y * matrix[2][1] + point.extra * matrix[2][2]

        point.x = new_x
        point.y = new_y
        point.extra = new_extra

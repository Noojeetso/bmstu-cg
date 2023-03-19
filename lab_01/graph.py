import itertools
from math import log
from tkinter import *

from functions import min_round
from storage import Point, Vector, Circle
from config import Config


class Graph(Canvas):
    canvas_width: int
    canvas_height: int
    config: Config
    min_offset: Vector
    offset: Vector
    min_point: list[float] = list([0, 0])
    max_point: list[float] = list([0, 0])
    max_diff: float
    precision = 3
    epsilon = 1e-3
    cursor_point: Point
    anchor_points: list[Point]
    center_points: list[Point]
    left_panel_points: list[Point]
    right_panel_points: list[Point]
    cursor_catch_radius = 10
    moving_point: Point | None
    grid_line_color: str
    circles: list[Circle]
    lines_heights: list[float]

    def __init__(self, master: Tk | Frame, width, height, config: Config):
        super().__init__(master, width=width, height=height)
        self.bind('<ButtonPress-1>', lambda event: self.cursor_dragging(event, 'press'))
        self.bind('<B1-Motion>', lambda event: self.cursor_dragging(event, 'move'))
        self.bind('<ButtonRelease-1>', lambda event: self.cursor_dragging(event, 'release'))

        self.config = config
        self.dot_radius = self.config.fields.get("point_radius")
        super().configure(bg=self.config.fields.get("graph_bg_color"))
        self.grid_line_color = self.config.fields.get("grid_line_color")

        self.anchor_points = list()
        self.center_points = list()
        self.min_offset = Vector(50, 50)
        self.offset = Vector(0, 0)

        self.circles = list()
        self.lines_heights = list()

        self.cursor_point = Point(0, 0)
        self.cursor_point.visible = False
        self.moving_point = None

    def run(self):
        self.mainloop()

    def resize(self):
        """ Process window resize """
        self.canvas_width = self.winfo_width()
        self.canvas_height = self.winfo_height()
        self.offset.x = self.min_offset.x
        self.offset.y = self.min_offset.y

        if self.canvas_width > self.canvas_height:
            self.offset.x += (self.canvas_width - self.canvas_height) / 2
        else:
            self.offset.y += (self.canvas_height - self.canvas_width) / 2

        self.update_min_max_points()
        self.draw()

    def change_precision(self, precision: int):
        self.precision = precision
        self.epsilon = 10 ** (-self.precision)

    def cursor_dragging(self, event, type_):
        """ Process dragging points on canvas """
        if type_ == 'press':
            min_point = None
            min_distance_squared = float("inf")
            radius = self.cursor_catch_radius
            points = itertools.chain(self.left_panel_points, self.right_panel_points)
            for point in points:
                canvas_x = self.real_to_canvas_x(point.x)
                canvas_y = self.real_to_canvas_y(point.y)

                distance_squared = pow(canvas_x - event.x, 2) + pow(canvas_y - event.y, 2)
                if distance_squared <= radius ** 2:
                    if min_point is None or min_distance_squared > distance_squared:
                        self.moving_point = point
                        min_distance_squared = distance_squared
        elif type_ == 'move':
            if self.moving_point is None:
                return
            self.follow_cursor(event.x, event.y)
        elif type_ == 'release':
            self.moving_point = None
            self.update_min_max_points()
            self.draw()

    def draw(self):
        """ Redraw graph on canvas """
        self.clear_graph()
        self.draw_graph()

    def clear_graph(self):
        self.delete("all")

    def set_circles(self, circles: list[Circle], lines_heights: list[float]):
        self.circles = circles
        self.lines_heights = lines_heights

    def draw_graph(self):
        self.draw_axes()

        self.anchor_points = list()
        self.center_points = list()

        for circle in self.circles:
            self.add_circle_anchors(circle.x, circle.y, circle.radius)

        self.update_min_max_points()

        python_green = "#476042"
        python_salmon = "#ff5733"
        radius = self.dot_radius
        meta_radius = 3

        for i, point in enumerate(self.left_panel_points):
            canvas_x = self.real_to_canvas_x(point.x)
            canvas_y = self.real_to_canvas_y(point.y)

            self.create_oval(canvas_x - radius, canvas_y - radius,
                             canvas_x + radius, canvas_y + radius, fill=python_green)
            self.create_text(canvas_x, canvas_y - 10, text=str(point),
                             fill="black", font=("Courier New", 10))

        for i, point in enumerate(self.right_panel_points):
            canvas_x = self.real_to_canvas_x(point.x)
            canvas_y = self.real_to_canvas_y(point.y)

            self.create_oval(canvas_x - radius, canvas_y - radius,
                             canvas_x + radius, canvas_y + radius, fill=python_salmon)
            self.create_text(canvas_x, canvas_y - 10, text=str(point),
                             fill="black", font=("Courier New", 10))

        for i, point in enumerate(self.center_points):
            canvas_x = self.real_to_canvas_x(point.x)
            canvas_y = self.real_to_canvas_y(point.y)

            self.create_oval(canvas_x - meta_radius, canvas_y - meta_radius,
                             canvas_x + meta_radius, canvas_y + meta_radius, fill="black")
            point_str = "[{1:.{0}3g}; {2:.{0}g}]".format(min(self.precision, 3), point.x, point.y)
            self.create_text(canvas_x, canvas_y - 10, text=point_str,
                             fill="black", font=("Courier New", 10))

        for circle in self.circles:
            self.draw_circle(circle.x, circle.y, circle.radius)

        for line_height in self.lines_heights:
            self.draw_line(line_height)

    def draw_axes(self):
        diff_x = self.max_point[0] - self.min_point[0]
        step_x = self.get_step(diff_x)
        diff_y = self.max_point[1] - self.min_point[1]
        step_y = self.get_step(diff_y)
        max_step = max(step_x, step_y)

        self.create_line(self.offset.x, self.canvas_height - 30, self.offset.x, 0, fill="red", width=3, arrow=LAST)
        self.create_line(0, self.canvas_height - self.offset.y, self.canvas_width, self.canvas_height - self.offset.y,
                         fill="red", width=3, arrow=LAST)

        if not self.left_panel_points and not self.right_panel_points:
            self.create_line(self.canvas_width // 2, self.canvas_height - self.offset.y - 5, self.canvas_width // 2,
                             self.canvas_height - self.offset.y + 5, width=2)
            self.create_line(self.offset.x - 5, self.canvas_height // 2, self.offset.x + 5,
                             self.canvas_height // 2, width=2)
            self.create_line(self.canvas_width // 2, self.canvas_height, self.canvas_width // 2, 0, width=2,
                             fill=self.grid_line_color)
            self.create_line(0, self.canvas_height // 2, self.canvas_width, self.canvas_height // 2, width=1,
                             fill=self.grid_line_color)
            num_str = "0"
            self.create_text(self.offset.x - 30, self.canvas_height // 2, text=num_str)
            self.create_text(self.canvas_width // 2, self.canvas_height - self.offset.y + 30, text=num_str)
            return

        if abs(self.max_point[0] - self.min_point[0]) < self.epsilon / 2:
            self.create_line(self.canvas_width // 2, self.canvas_height, self.canvas_width // 2, 0, width=2,
                             fill=self.grid_line_color)
            self.create_line(self.canvas_width // 2, self.canvas_height - self.offset.y - 5, self.canvas_width // 2,
                             self.canvas_height - self.offset.y + 5, width=2)
            print_precision = min(self.precision, 3) + 1
            abs_val = abs(self.min_point[0])
            if abs_val >= self.epsilon:
                num_str = "{0:.{1:}g}".format(self.min_point[0], print_precision)
            else:
                num_str = "0"
            self.create_text(self.canvas_width // 2, self.canvas_height - self.offset.y + 30, text=num_str)
        else:
            i = self.min_point[0] - self.min_point[0] % max_step
            x = self.real_to_canvas_x(i)
            while x < self.canvas_width:
                if abs(x - self.offset.x) > 1:
                    self.create_line(x, 0, x, self.canvas_height, width=2, fill=self.grid_line_color)
                self.create_line(x, self.canvas_height - self.offset.y - 5,
                                 x, self.canvas_height - self.offset.y + 5, width=2)
                print_precision = min(self.precision, 3) + 1
                abs_val = abs(i)
                if abs_val >= self.epsilon:
                    num_str = "{0:.{1:}g}".format(i, print_precision)
                else:
                    num_str = "0"

                self.create_text(x, self.canvas_height - self.offset.y + 30, text=num_str)
                i += max_step
                x = self.real_to_canvas_x(i)

        if abs(self.max_point[1] - self.min_point[1]) < self.epsilon / 2:
            self.create_line(0, self.canvas_height // 2, self.canvas_width, self.canvas_height // 2, width=1,
                             fill=self.grid_line_color)
            self.create_line(self.offset.x - 5, self.canvas_height // 2, self.offset.x + 5,
                             self.canvas_height // 2, width=2)
            print_precision = min(self.precision, 3) + 1
            abs_val = abs(self.min_point[1])
            if abs_val >= self.epsilon:
                # num_str = "{0:.{1:}{c}}".format(i, print_precision, c='g' if abs_val > 1e3 or abs_val < 1e-3 else 'g')
                num_str = "{0:.{1:}g}".format(self.min_point[1], print_precision)
            else:
                num_str = "0"

            self.create_text(self.offset.x - 30, self.canvas_height // 2, text=num_str)
        else:
            i = self.min_point[1] - self.min_point[1] % max_step
            y = self.real_to_canvas_y(i)
            while y > 0:
                if abs(y - (self.canvas_height - self.offset.y)) > 1:
                    self.create_line(0, y, self.canvas_width, y, width=1, fill=self.grid_line_color)
                self.create_line(self.offset.x - 5, y, self.offset.x + 5, y, width=2)
                print_precision = min(self.precision, 3) + 1
                abs_val = abs(i)
                if abs_val >= self.epsilon:
                    num_str = "{0:.{1:}g}".format(i, print_precision)
                else:
                    num_str = "0"
                self.create_text(self.offset.x - 30, y, text=num_str)
                i += max_step
                y = self.real_to_canvas_y(i)

    def get_step(self, diff: float) -> float:
        if abs(diff) <= self.epsilon or abs(diff) == float("inf"):
            return 1
        # print(diff)
        raw_dec_power = log(diff) / log(10)
        dec_power = min_round(raw_dec_power)
        step = 10 ** dec_power

        while diff / step <= 2 and step >= self.epsilon:
            step /= 10
        return step

    def to_real_x(self, canvas_x: float) -> float:
        graph_width = self.canvas_width - 2 * self.offset.x
        if abs(graph_width) < self.epsilon / 2:
            real_x = self.min_point[0]
        else:
            real_x = (self.max_diff * (canvas_x - self.offset.x) / graph_width) + self.min_point[0]
        return real_x

    def to_real_y(self, canvas_y: float) -> float:
        graph_height = self.canvas_height - 2 * self.offset.y
        if abs(graph_height) < self.epsilon / 2:
            real_y = self.min_point[1]
        else:
            real_y = (self.max_diff * (self.canvas_height - self.offset.y - canvas_y) /
                      graph_height) + self.min_point[1]
        return real_y

    def real_to_canvas_x(self, real_x: float) -> int:
        if abs(self.max_point[0] - self.min_point[0]) < self.epsilon / 2:
            # print(abs(self.max_diff), self.epsilon)
            return self.canvas_width // 2

        relative_x = real_x - self.min_point[0]
        canvas_x = self.offset.x + (self.canvas_width - 2 * self.offset.x) * relative_x / self.max_diff

        return int(canvas_x)

    def real_to_canvas_y(self, real_y: float) -> int:
        if abs(self.max_point[1] - self.min_point[1]) < self.epsilon / 2:
            return self.canvas_height // 2

        relative_y = real_y - self.min_point[1]
        canvas_y = self.canvas_height - self.offset.y - (self.canvas_height - 2 * self.offset.y) * relative_y / self.max_diff

        return int(canvas_y)

    def update_min_max_points(self):
        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")

        points = itertools.chain(self.left_panel_points, self.right_panel_points, self.anchor_points)
        for point in points:
            min_x = min(point.x, min_x)
            max_x = max(point.x, max_x)
            min_y = min(point.y, min_y)
            max_y = max(point.y, max_y)
        self.min_point = [min_x, min_y]
        self.max_point = [max_x, max_y]
        diff_x = max_x - min_x
        diff_y = max_y - min_y
        self.max_diff = max(diff_x, diff_y)

    def follow_cursor(self, cursor_canvas_x: float, cursor_canvas_y: float):
        real_x = self.to_real_x(cursor_canvas_x)
        real_y = self.to_real_y(cursor_canvas_y)

        points = itertools.chain(self.left_panel_points, self.right_panel_points)
        for point in points:
            if abs(point.x - real_x) < self.epsilon / 2 and abs(point.y - real_y) < self.epsilon / 2:
                return

        self.moving_point.x = round(real_x, self.precision)
        self.moving_point.y = round(real_y, self.precision)

        self.moving_point.x_var.set(self.moving_point.x)
        self.moving_point.y_var.set(self.moving_point.y)

        self.update_min_max_points()
        self.draw()

    def draw_line(self, real_height: float):
        canvas_y = self.real_to_canvas_y(real_height)
        self.create_line(0, canvas_y, self.canvas_width, canvas_y)

    def add_circle_anchors(self, real_x, real_y, radius):
        new_point = Point(real_x + radius, real_y)
        self.anchor_points.append(new_point)
        new_point = Point(real_x, real_y + radius)
        self.anchor_points.append(new_point)
        new_point = Point(real_x - radius, real_y)
        self.anchor_points.append(new_point)
        new_point = Point(real_x, real_y - radius)
        self.anchor_points.append(new_point)
        new_point = Point(real_x, real_y)
        self.center_points.append(new_point)
        self.update_min_max_points()

    def draw_circle(self, real_x, real_y, radius):
        x = self.real_to_canvas_x(real_x)
        y = self.real_to_canvas_y(real_y)

        radius_x = self.real_to_canvas_x(real_x + radius)
        radius = radius_x - x

        self.create_oval(x - radius, y - radius, x + radius, y + radius)

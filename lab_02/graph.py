from PyQt5.QtCore import Qt

from storage import Point, Figure, IntVector, FloatVector, Line
from config import Config
from PyQt5.QtGui import QPainter, QPaintEvent, QResizeEvent, QColor
from PyQt5.QtWidgets import QWidget


class GraphicsWidget(QWidget):
    resized = False

    def __init__(self, widget: QWidget):
        super().__init__(widget)
        print("rect:", self.rect())
        self.width = self.rect().width()
        self.height = self.rect().height()
        self.graph = Graph(self.width, self.height)

    def paintEvent(self, event: QPaintEvent) -> None:
        rect = event.rect()
        print("Drawing")
        print(rect)

        painter = QPainter(self)
        # painter.translate(0, self.height)
        # painter.scale(1, -1)
        pen = painter.pen()
        pen.setWidth(1)
        painter.setPen(pen)

        painter.save()

        self.graph.draw(painter)

        painter.restore()

    def resizeEvent(self, event: QResizeEvent):
        self.width = event.size().width()
        self.height = event.size().height()
        # self.graph.resize(self.width, self.height)
        self.graph.resize(800, 500)

        if not self.resized:
            self.graph.move_to_center()
            self.graph.figure.history_prev.clear()
            self.graph.figure.history_next.clear()
            self.resized = True


class Graph:
    canvas_width: int
    canvas_height: int
    config: Config
    precision = 3
    epsilon = 1e-3
    figure: Figure

    def __init__(self, width: int, height: int):  # , config: Config):
        self.figure = Figure(width // 2, height // 2, 100)
        self.canvas_width = width
        self.canvas_height = height
        # self.config = config
        # super().configure(bg=self.config.fields.get("graph_bg_color"))
        # self.grid_line_color = self.config.fields.get("grid_line_color")

    def draw(self, painter: QPainter):
        # drawable_points = self.figure.get_drawable_points()

        last_point = self.figure.astroid.points[0]
        for point in self.figure.astroid.points[1:]:
            self.draw_line_from_points(painter, last_point, point)
            last_point = point
        self.draw_line_from_points(painter, last_point, self.figure.astroid.points[0])

        last_point = self.figure.circle.points[0]
        for point in self.figure.circle.points[1:]:
            self.draw_line_from_points(painter, last_point, point)
            last_point = point
        self.draw_line_from_points(painter, last_point, self.figure.circle.points[0])

        for line in self.figure.get_lines():
            self.draw_line(painter, line)

        self.draw_point(painter, self.figure.center)

    def draw_point(self, painter: QPainter, point: Point):
        pen = painter.pen()
        pen.setWidth(8)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(QColor(220, 76, 79, 255))
        painter.setPen(pen)

        x, y = int(point.x), self.canvas_height - int(point.y)
        painter.drawPoint(x, y)

        pen.setWidth(1)
        pen.setCapStyle(Qt.SquareCap)
        pen.setColor(QColor(0, 0, 0, 255))
        painter.setPen(pen)

        painter.drawText(x - len(str(point)) * 3, y - 7, str(point))

    def draw_line_from_points(self, painter: QPainter, point_a: Point, point_b: Point):
        painter.drawLine(int(point_a.x), self.canvas_height - int(point_a.y),
                         int(point_b.x), self.canvas_height - int(point_b.y))

    def draw_line(self, painter: QPainter, line: Line):
        point_a = line.start
        point_b = line.end
        painter.drawLine(int(point_a.x), self.canvas_height - int(point_a.y),
                         int(point_b.x), self.canvas_height - int(point_b.y))

    def move_to_center(self):
        self.figure.move_to_center(self.canvas_width / 2, self.canvas_height / 2)

    def resize(self, width: int, height: int):
        """ Process window resize """
        self.canvas_width = width
        self.canvas_height = height

    def move(self, diff_x: float, diff_y: float):
        self.figure.move(diff_x, diff_y)

    def scale(self, center: FloatVector, scale: FloatVector):
        self.figure.scale(center, scale)

    def rotate(self, center: FloatVector, angle_degrees: float):
        self.figure.rotate(center, angle_degrees)

    # def draw_axes(self):
    #     # diff_x = self.max_point[0] - self.min_point[0]
    #     # step_x = self.get_step(diff_x)
    #     # diff_y = self.max_point[1] - self.min_point[1]
    #     # step_y = self.get_step(diff_y)
    #     # max_step = max(step_x, step_y)
    #     max_step = 1
    #
    #     self.create_line(self.offset.x, self.canvas_height - 30, self.offset.x, 0, fill="red", width=3, arrow=LAST)
    #     self.create_line(0, self.canvas_height - self.offset.y, self.canvas_width, self.canvas_height - self.offset.y,
    #                      fill="red", width=3, arrow=LAST)
    #
    #     if abs(self.max_diff) < self.epsilon:
    #         self.create_line(self.canvas_width // 2, self.canvas_height, self.canvas_width // 2, 0, width=2,
    #                          fill=self.grid_line_color)
    #         self.create_line(self.canvas_width // 2, self.canvas_height - self.offset.y - 5, self.canvas_width // 2,
    #                          self.canvas_height - self.offset.y + 5, width=2)
    #         print_precision = min(self.precision, 3)
    #         abs_val = abs(self.min_point[0])
    #         if abs_val >= self.epsilon:
    #             num_str = "{0:.{1:}g}".format(self.min_point[0], print_precision)
    #         else:
    #             num_str = "0"
    #
    #         self.create_text(self.canvas_width // 2, self.canvas_height - self.offset.y + 30, text=num_str)
    #
    #         self.create_line(0, self.canvas_height // 2, self.canvas_width, self.canvas_height // 2, width=1,
    #                          fill=self.grid_line_color)
    #         self.create_line(self.offset.x - 5, self.canvas_height // 2, self.offset.x + 5,
    #                          self.canvas_height // 2, width=2)
    #         print_precision = min(self.precision, 3)
    #         abs_val = abs(self.min_point[1])
    #         if abs_val >= self.epsilon:
    #             # num_str = "{0:.{1:}{c}}".format(i, print_precision, c='g' if abs_val > 1e3 or abs_val < 1e-3 else 'g')
    #             num_str = "{0:.{1:}g}".format(self.min_point[1], print_precision)
    #         else:
    #             num_str = "0"
    #
    #         self.create_text(self.offset.x - 30, self.canvas_height // 2, text=num_str)
    #         return
    #
    #     i = self.min_point[0] - self.min_point[0] % max_step
    #     x = self.real_to_canvas_x(i)
    #     while x < self.canvas_width:
    #         if abs(x - self.offset.x) > 1:
    #             self.create_line(x, 0, x, self.canvas_height, width=2, fill=self.grid_line_color)
    #         self.create_line(x, self.canvas_height - self.offset.y - 5,
    #                          x, self.canvas_height - self.offset.y + 5, width=2)
    #         print_precision = min(self.precision, 3)
    #         abs_val = abs(i)
    #         if abs_val >= self.epsilon:
    #             num_str = "{0:.{1:}g}".format(i, print_precision)
    #         else:
    #             num_str = "0"
    #
    #         self.create_text(x, self.canvas_height - self.offset.y + 30, text=num_str)
    #         i += max_step
    #         x = self.real_to_canvas_x(i)
    #
    #     i = self.min_point[1] - self.min_point[1] % max_step
    #     y = self.real_to_canvas_y(i)
    #     while y > 0:
    #         if abs(y - (self.canvas_height - self.offset.y)) > 1:
    #             self.create_line(0, y, self.canvas_width, y, width=1, fill=self.grid_line_color)
    #         self.create_line(self.offset.x - 5, y, self.offset.x + 5, y, width=2)
    #         print_precision = min(self.precision, 3)
    #         abs_val = abs(i)
    #         if abs_val >= self.epsilon:
    #             num_str = "{0:.{1:}g}".format(i, print_precision)
    #         else:
    #             num_str = "0"
    #
    #         self.create_text(self.offset.x - 30, y, text=num_str)
    #         i += max_step
    #         y = self.real_to_canvas_y(i)

    # def get_step(self, diff: float) -> float:
    #     if abs(diff) <= self.epsilon:
    #         return self.epsilon
    #     raw_dec_power = log(diff) / log(10)
    #     dec_power = min_round(raw_dec_power)
    #     step = 10 ** dec_power
    #
    #     # print(diff/step)
    #     while diff / step <= 2:
    #         step /= 10
    #     return step

    def real_to_canvas_x(self, real_x: float) -> int:
        # relative_x = real_x - self.min_point[0]
        # canvas_x = self.offset.x + real_x
        # + (self.canvas_width - 2 * self.offset.x) * relative_x / self.max_diff

        return int(real_x)

    def real_to_canvas_y(self, real_y: float) -> int:
        # relative_y = real_y - self.min_point[1]
        canvas_y = self.canvas_height - real_y
        # - (self.canvas_height - 2 * self.offset.y) * relative_y / self.max_diff

        return int(canvas_y)

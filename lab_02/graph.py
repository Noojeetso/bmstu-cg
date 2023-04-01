from PyQt5.QtCore import Qt

from storage import Point, Figure, FloatVector, Line
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
        painter = QPainter(self)
        pen = painter.pen()
        pen.setWidth(1)
        painter.setPen(pen)

        painter.save()

        self.graph.draw(painter)

        painter.restore()

    def resizeEvent(self, event: QResizeEvent):
        self.width = event.size().width()
        self.height = event.size().height()
        self.graph.resize(self.width, self.height)

        if not self.resized:
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
    left_point: Point
    bottom_point: Point
    top_point: Point
    right_point: Point

    def __init__(self, width: int, height: int):
        self.figure = Figure(0, 0, 100)
        self.canvas_width = width
        self.canvas_height = height
        self.left_point = Point(0, self.canvas_height // 2)
        self.right_point = Point(self.canvas_width, self.canvas_height // 2)
        self.top_point = Point(self.canvas_width // 2, self.canvas_height)
        self.bottom_point = Point(self.canvas_width // 2, 0)
        self.red = QColor(220, 76, 79, 255)
        self.black = QColor(0, 0, 0, 255)

    def draw(self, painter: QPainter):
        pen = painter.pen()
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

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

        pen.setWidth(1)
        pen.setCapStyle(Qt.SquareCap)
        pen.setColor(self.black)
        painter.setPen(pen)

        self.draw_point(painter, self.figure.center)

        self.draw_axes(painter)

    def draw_point(self, painter: QPainter, point: Point):
        pen = painter.pen()
        pen.setWidth(8)
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self.red)
        painter.setPen(pen)

        x, y = int(point.x + self.canvas_width / 2), self.canvas_height - int(point.y + self.canvas_height / 2)
        painter.drawPoint(x, y)

        pen.setWidth(1)
        pen.setCapStyle(Qt.SquareCap)
        pen.setColor(self.black)
        painter.setPen(pen)

        painter.drawText(x - len(str(point)) * 3, y - 7, str(point))

    def draw_axes(self, painter: QPainter):
        painter.drawLine(int(self.left_point.x), self.canvas_height - int(self.left_point.y),
                         int(self.right_point.x), self.canvas_height - int(self.right_point.y))
        painter.drawLine(int(self.bottom_point.x), self.canvas_height - int(self.bottom_point.y),
                         int(self.top_point.x), self.canvas_height - int(self.top_point.y))

    def draw_line_from_points(self, painter: QPainter, point_a: Point, point_b: Point):
        painter.drawLine(int(point_a.x + self.canvas_width / 2),
                         self.canvas_height - int(point_a.y + self.canvas_height / 2),
                         int(point_b.x + self.canvas_width / 2),
                         self.canvas_height - int(point_b.y + self.canvas_height / 2))

    def draw_line(self, painter: QPainter, line: Line):
        point_a = line.start
        point_b = line.end
        painter.drawLine(int(point_a.x + self.canvas_width / 2),
                         self.canvas_height - int(point_a.y + self.canvas_height / 2),
                         int(point_b.x + self.canvas_width / 2),
                         self.canvas_height - int(point_b.y + self.canvas_height / 2))

    def resize(self, width: int, height: int):
        """ Process window resize """
        self.canvas_width = width
        self.canvas_height = height
        self.left_point = Point(0, self.canvas_height // 2)
        self.right_point = Point(self.canvas_width, self.canvas_height // 2)
        self.top_point = Point(self.canvas_width // 2, self.canvas_height)
        self.bottom_point = Point(self.canvas_width // 2, 0)

    def move(self, diff_x: float, diff_y: float):
        self.figure.move(diff_x, diff_y)

    def scale(self, center: FloatVector, scale: FloatVector):
        self.figure.scale(center, scale)

    def rotate(self, center: FloatVector, angle_degrees: float):
        self.figure.rotate(center, angle_degrees)

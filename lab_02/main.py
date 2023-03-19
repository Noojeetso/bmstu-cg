import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox
from form import Ui_MainWindow
from storage import Point, IntVector, FloatVector, Figure


class MainWindow(QMainWindow):
    width: int
    height: int
    precision = 3
    epsilon = 1e-3

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect()
        self.setWindowTitle("КГ Лабораторная № 02")
        # uic.loadUi("form.py", self)

    @staticmethod
    def get_field_value(input_field: QLineEdit) -> float:
        try:
            value = input_field.text()
            value = float(value)
        except ValueError:
            print("Incorrect field values")
            raise ValueError

        return value

    def transit(self):
        try:
            diff_x = self.get_field_value(self.ui.input_local_transition_x)
            diff_x = int(diff_x)
            diff_y = self.get_field_value(self.ui.input_local_transition_y)
            diff_y = int(diff_y)
        except ValueError:
            return

        self.graph_move(IntVector(diff_x, diff_y))

    def graph_move(self, diff: IntVector):
        self.ui.graphics_widget.graph.move(diff.x, diff.y)
        self.ui.graphics_widget.update()

    def scale(self):
        try:
            scale_kx = self.get_field_value(self.ui.input_scale_kx)
            scale_ky = self.get_field_value(self.ui.input_scale_ky)
            x = self.get_field_value(self.ui.input_scale_x)
            y = self.get_field_value(self.ui.input_scale_y)
        except ValueError:
            return

        self.graph_scale(FloatVector(x, y), FloatVector(scale_kx, scale_ky))

    def graph_scale(self, center: FloatVector, scale: FloatVector):
        self.ui.graphics_widget.graph.scale(center, scale)
        self.ui.graphics_widget.update()

    def rotate(self):
        try:
            angle_degrees = self.get_field_value(self.ui.input_rotation_angle)
            x = self.get_field_value(self.ui.input_rotation_x)
            y = self.get_field_value(self.ui.input_rotation_y)
        except ValueError:
            return

        self.graph_rotate(FloatVector(x, y), angle_degrees)

    def graph_rotate(self, center: FloatVector, angle_degrees: float):
        self.ui.graphics_widget.graph.rotate(center, angle_degrees)
        self.ui.graphics_widget.update()

    def undo(self):
        if not self.ui.graphics_widget.graph.figure.history_prev:
            QMessageBox.warning(self, "Предупреждение", "Предыдущих действий нет")
            return
        self.ui.graphics_widget.graph.figure.undo()
        self.ui.graphics_widget.update()

    def redo(self):
        if not self.ui.graphics_widget.graph.figure.history_next:
            QMessageBox.warning(self, "Предупреждение", "Дальше действий нет")
            return
        self.ui.graphics_widget.graph.figure.redo()
        self.ui.graphics_widget.update()

    def init_figure(self):
        try:
            radius = self.get_field_value(self.ui.input_radius)
        except ValueError:
            return

        self.ui.graphics_widget.graph.figure.history_next.clear()
        self.ui.graphics_widget.graph.figure.history_prev.clear()
        width = self.ui.graphics_widget.graph.canvas_width
        height = self.ui.graphics_widget.graph.canvas_height
        self.ui.graphics_widget.graph.figure = Figure(width / 2, height / 2, radius)
        self.ui.graphics_widget.update()

    def transition_info(self):
        QMessageBox.about(self, "Смещение", "X - смещение по оси абсцисс\n"
                                            "Y - смещение по оси ординат")

    def rotation_info(self):
        QMessageBox.about(self, "Поворот", "Угол - угол поворота в градусах (вращение против часовой стрелке)\n"
                                           "X - абсцисса центра вращения\n"
                                           "Y - ордината центра вращения")

    def scale_info(self):
        QMessageBox.about(self, "Масштабирование", "kX - коэффициент масштабирования по оси абсцисс\n"
                                                   "kY - коэффициент масштабирования по оси ординат\n"
                                                   "X - абсцисса центра масштабирования\n"
                                                   "Y - ордината центра масштабирования")

    def reset_info(self):
        QMessageBox.about(self, "Сброс фигуры", "Радиус - начальное значение радиуса, используемого для построения фигуры\n"
                                                "Примечание: при сбрасывании фигуры также стирается история преобразованй")

    def about(self):
        QMessageBox.about(self, "О программе", "Программа осуществляет следующие преобразования над фигурой:\n"
                                               " - Перенос\n"
                                               " - Вращение относительно точки\n"
                                               " - Масштабирование относительно точки\n"
                                               "Фигура состоит из:\n"
                                               "Астроиды:\n"
                                               " - уравнения:\n"
                                               "\t x = cos(t) ^ 3 * r\n"
                                               "\t y = sin(t) ^ 3 * r\n"
                                               "Окружности:\n"
                                               " - уравнения:\n"
                                               "\t x = sin(t) * r / 3\n"
                                               "\t y = cos(t) * r / 3\n"
                                               "Трёх прямых, каждая длиной 2 * r,\n"
                                               "образующих квадрат без верхнего ребра,\n"
                                               "причём две из прямых касаются концов астроиды справа и слева\n"
                                               "r - значение радиуса\n"
                                               "Ось абсцисс направлена слева направо\n"
                                               "Ось ординат направлена снизу вверх")

    def connect(self):
        self.ui.apply_local_transition.clicked.connect(self.transit)
        self.ui.apply_scale.clicked.connect(self.scale)
        self.ui.apply_rotation.clicked.connect(self.rotate)
        self.ui.apply_undo.clicked.connect(self.undo)
        self.ui.apply_redo.clicked.connect(self.redo)
        self.ui.init_figure.clicked.connect(self.init_figure)
        self.ui.scale_info.clicked.connect(self.scale_info)
        self.ui.transition_info.clicked.connect(self.transition_info)
        self.ui.rotation_info.clicked.connect(self.rotation_info)
        self.ui.reset_info.clicked.connect(self.reset_info)
        self.ui.action.triggered.connect(self.about)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

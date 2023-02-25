import itertools
from tkinter import *
from functions import solve
from graph import Graph
from panel import Panel
from storage import PointTable, Point
from tkinter import messagebox

LEFT_PANEL = "left_panel"
RIGHT_PANEL = "right_panel"


class App(Tk):
    width: int
    height: int
    frame_widgets: list[Widget] = list()
    precision = 3
    epsilon = 1e-3
    graph: Graph

    def __init__(self):
        super().__init__()
        self.geometry("1150x510")
        self.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.resizable = (0, 0)

        self.title("CG Lab 01")
        self.bind('<Configure>', lambda event: self.resize())

        top_panel = Frame(self)
        top_panel.pack(side=TOP, expand=False, fill=BOTH)

        precision_label = Label(top_panel, text="Precision:")
        precision_label.pack(side=LEFT, expand=False, fill=BOTH)

        self.precision_box_var = StringVar()
        self.precision_box_var.set(str(self.precision))
        self.precision_box = Spinbox(top_panel, from_=0, to=5, textvariable=self.precision_box_var,
                                     command=self.change_precision)
        self.precision_box.pack(side=LEFT, expand=False, fill=BOTH)
        solve_button = Button(top_panel, text="Solve")
        solve_button.pack(side=RIGHT, expand=True, fill=BOTH)

        self.left_panel = Panel(LEFT, self.precision)
        self.left_panel.bind("<<OnAppend>>", lambda event: self.on_append(LEFT_PANEL))
        self.left_panel.bind("<<OnRemove>>", lambda event: self.on_remove())
        self.left_panel.bind("<<OnMove>>", lambda event: self.on_move())

        self.graph = Graph(self, self.height, self.height)
        self.graph.pack(side=LEFT, expand=True, fill=BOTH)

        self.right_panel = Panel(RIGHT, self.precision)
        self.right_panel.bind("<<OnAppend>>", lambda event: self.on_append(RIGHT_PANEL))
        self.right_panel.bind("<<OnRemove>>", lambda event: self.on_remove())
        self.right_panel.bind("<<OnMove>>", lambda event: self.on_move())

        self.graph.left_panel_points = self.left_panel.points
        self.graph.right_panel_points = self.right_panel.points

        solve_button.configure(command=self.solve)

        table_left = PointTable()
        table_left.from_file("table_left.txt")
        for point in table_left.points:
            self.left_panel.create_point_frame(round(point.x, self.precision), round(point.y, self.precision))

        table_right = PointTable()
        table_right.from_file("table_right.txt")
        for point in table_right.points:
            self.right_panel.create_point_frame(round(point.x, self.precision), round(point.y, self.precision))

    def run(self):
        self.mainloop()

    def resize(self):
        """ Process window resize """
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.graph.resize()

    @staticmethod
    def points_equal(point_a: Point, point_b: Point, epsilon: int):
        if abs(point_a.x - point_b.x) >= epsilon:
            return False
        if abs(point_a.y - point_b.y) >= epsilon:
            return False
        return True

    def check_precision_update(self, new_precision: int):
        def rollback():
            points: list[Point] = self.left_panel.points + self.right_panel.points
            for point in points:
                point.x = point.x_var.get()
                point.y = point.y_var.get()

        points: list[Point] = self.left_panel.points + self.right_panel.points
        new_epsilon = 10 ** (-new_precision)

        points: list[Point] = [point.round(new_precision) for point in points]

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if self.points_equal(points[i], points[j], new_epsilon):
                    messagebox.showerror('Ошибка преобразования',
                                         'Невозможно изменить точность: некоторые точки будут совпадать')
                    rollback()
                    return False
        return True

    def change_precision(self):
        new_precision = int(self.precision_box.get())
        if not self.check_precision_update(new_precision):
            self.precision_box_var.set(str(self.precision))
            return
        self.precision = new_precision
        self.epsilon = 10 ** (-self.precision)

        self.left_panel.precision = new_precision
        self.right_panel.precision = new_precision
        points = itertools.chain(self.left_panel.points, self.right_panel.points)
        for point in points:
            point.round(new_precision)
            point.update_vars()

        self.graph.change_precision(self.precision)

    def on_remove(self):
        self.graph.update_min_max_points()
        self.graph.draw()

    def on_append(self, panel: str):
        new_point: Point

        if panel == RIGHT_PANEL:
            new_point = self.right_panel.points[-1]
            points = itertools.chain(self.left_panel.points, self.right_panel.points[:-1])
            for point in points:
                if self.points_equal(point, new_point, self.epsilon):
                    self.right_panel.remove_point_frame(self.right_panel.point_frames[-1])
                    messagebox.showwarning('Ошибка создания точки',
                                           'Данная точка уже существует')
                    break
        elif panel == LEFT_PANEL:
            new_point = self.left_panel.points[-1]
            points = itertools.chain(self.right_panel.points, self.left_panel.points[:-1])
            for point in points:
                if self.points_equal(point, new_point, self.epsilon):
                    self.left_panel.remove_point_frame(self.left_panel.point_frames[-1])
                    messagebox.showwarning('Ошибка создания точки',
                                           'Данная точка уже существует')
                    break
        else:
            raise ValueError

        # x = new_point.x
        # y = new_point.y
        # if not (self.max_point[0] > x > self.min_point[0] and
        #         self.min_point[1] < y < self.max_point[1]):
        self.graph.update_min_max_points()
        self.graph.draw()

    def on_move(self):
        self.graph.update_min_max_points()
        self.graph.draw()

    def solve(self):
        circles, used_circles, line_heights = solve(self.left_panel.points, self.right_panel.points, self.epsilon)

        if not circles:
            messagebox.showerror("Ошибка решения",
                                 "Невозможно построить ни одной окружности")
            return

        if not used_circles:
            messagebox.showerror("Ошибка решения",
                                 "Ни одна пара окружностей не удовлетворяет условиям")
            return

        self.graph.draw_circles(used_circles)

        for line_height in line_heights:
            self.graph.draw_line(line_height)

        # self.graph.anchor_points = list()

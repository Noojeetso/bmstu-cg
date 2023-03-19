import itertools
from tkinter import *
from functions import solve
from graph import Graph
from panel import Panel
from storage import PointTable, Point, Circle
from tkinter import messagebox
from config import Config

LEFT_PANEL = "left_panel"
RIGHT_PANEL = "right_panel"


class App(Tk):
    width: int
    height: int
    frame_widgets: list[Widget] = list()
    precision = 3
    epsilon = 1e-3
    graph: Graph
    config: Config

    def __init__(self):
        super().__init__()

        self.geometry("1150x510")
        self.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.resizable = (0, 0)

        self.title("CG Lab 01")
        self.bind('<Configure>', lambda event: self.resize())

        self.config = Config()
        self.tk_setPalette(background=self.config.fields.get("bg_color"),
                           activeBackground=self.config.fields.get("active_bg_color"))

        main_menu = Menu(self)
        super().config(menu=main_menu)
        main_menu.add_command(label="О программе", command=self.about_task)

        top_panel = Frame(self)
        top_panel.pack(side=TOP, expand=False, fill=BOTH)

        precision_label = Label(top_panel, text=" Точность:")
        precision_label.pack(side=LEFT, expand=False, fill=BOTH)

        self.precision_box_var = StringVar()
        self.precision_box_var.set(str(self.precision))
        self.precision_box = Spinbox(top_panel, from_=0, to=5, textvariable=self.precision_box_var,
                                     command=self.change_precision, bg=self.config.fields.get("field_color"))
        self.precision_box.pack(side=LEFT, expand=False, fill=BOTH)
        solve_button = Button(top_panel, text="Решить", bg=self.config.fields.get("fg_color"),
                              activebackground=self.config.fields.get("active_bg_color"))
        solve_button.pack(side=RIGHT, expand=True, fill=BOTH)

        self.left_panel = Panel(LEFT, self.precision, self.config)
        self.left_panel.bind("<<OnAppend>>", lambda event: self.on_append(LEFT_PANEL))
        self.left_panel.bind("<<OnRemove>>", lambda event: self.on_remove())
        self.left_panel.bind("<<OnMove>>", lambda event: self.on_move(LEFT_PANEL, event))

        self.graph = Graph(self, self.height, self.height, self.config)
        self.graph.pack(side=LEFT, expand=True, fill=BOTH)

        self.right_panel = Panel(RIGHT, self.precision, self.config)
        self.right_panel.bind("<<OnAppend>>", lambda event: self.on_append(RIGHT_PANEL))
        self.right_panel.bind("<<OnRemove>>", lambda event: self.on_remove())
        self.right_panel.bind("<<OnMove>>", lambda event: self.on_move(RIGHT_PANEL, event))

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
        self.right_panel.update_indices()
        self.left_panel.update_indices()

    @staticmethod
    def about_task():
        messagebox.showinfo("О программе", "На плоскости заданы два множества точек.\n"
                                           "Найти все пары окружностей, каждая из которых проходит "
                                           "хотя бы через три разные точки одного и того же множества таких, "
                                           "что касательная проведённая к обеим окружностям (внешняя) "
                                           "параллельна оси абсцисс.\n"
                                           "Сделать в графическом режиме вывод изображения.")

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
            points = itertools.chain(self.left_panel.points, self.right_panel.points)
            for point in points:
                point.x = point.x_var.get()
                point.y = point.y_var.get()

        points = itertools.chain(self.left_panel.points, self.right_panel.points)
        new_epsilon = 10 ** (-new_precision)

        points = [point.round(new_precision) for point in points]

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
        self.left_panel.update_indices()
        self.right_panel.update_indices()
        self.graph.update_min_max_points()
        self.graph.draw()

    def on_append(self, panel: str):
        new_point: Point

        if panel == RIGHT_PANEL:
            new_point = self.right_panel.points[-1]
            for i in range(len(self.right_panel.points) - 1):
                point = self.right_panel.points[i]

                if self.points_equal(point, new_point, self.epsilon):
                    self.right_panel.remove_point_frame(self.right_panel.point_frames[-1])
                    messagebox.showwarning('Ошибка создания точки',
                                           'Данная точка уже существует')
                    break
            self.right_panel.update_indices()
        elif panel == LEFT_PANEL:
            new_point = self.left_panel.points[-1]
            for i in range(len(self.left_panel.points) - 1):
                point = self.left_panel.points[i]

                if self.points_equal(point, new_point, self.epsilon):
                    self.left_panel.remove_point_frame(self.left_panel.point_frames[-1])
                    messagebox.showwarning('Ошибка создания точки',
                                           'Данная точка уже существует')
                    break
            self.left_panel.update_indices()
        else:
            raise ValueError

        # x = new_point.x
        # y = new_point.y
        # if not (self.max_point[0] > x > self.min_point[0] and
        #         self.min_point[1] < y < self.max_point[1]):
        self.graph.update_min_max_points()
        self.graph.draw()

    def on_move(self, side: str, event: Event):
        curr_point: Point

        if side == LEFT_PANEL:
            curr_point = self.left_panel.points[event.state]
        elif side == RIGHT_PANEL:
            curr_point = self.right_panel.points[event.state]
        else:
            raise ValueError

        curr_point_x = curr_point.x_var.get()
        curr_point_y = curr_point.y_var.get()
        points = itertools.chain(self.left_panel.points, self.right_panel.points)
        for point in points:
            if abs(curr_point_x - point.x) < self.epsilon / 2 and abs(curr_point_y - point.y) < self.epsilon / 2:
                curr_point.x_var.set(curr_point.x)
                curr_point.y_var.set(curr_point.y)
                return

        curr_point.x = round(curr_point_x, self.precision)
        curr_point.y = round(curr_point_y, self.precision)
        self.graph.update_min_max_points()
        self.graph.draw()

    def solve(self):
        circles, used_circles, line_heights = solve(self.left_panel.points, self.right_panel.points, self.epsilon)

        self.graph.set_circles(used_circles, line_heights)
        self.graph.draw()

        if not circles:
            messagebox.showerror("Ошибка решения",
                                 "Невозможно построить ни одной окружности")
            return

        if not used_circles:
            messagebox.showerror("Ошибка решения",
                                 "Ни одна пара окружностей не удовлетворяет условиям")
            return
        self.print_answer(used_circles, line_heights)

    def print_answer(self, used_circles: list[Circle], heights: [float]):
        str_answer = ""
        print(len(used_circles), len(heights), heights)
        index = 1
        for circle in used_circles:
            if index % 2 == 1:
                str_answer += "Решение №" + str(index // 2 + 1) + "\n\n"
            height_str = "\n"
            print_precision = min(self.precision, 3)
            if index % 2 == 1:
                circle_str = "Первая окружность:\n"
                circle_str += "Координаты:\n" + "X: " + str(round(circle.x, print_precision)) + " Y: " + str(round(circle.y, print_precision)) + '\n'
                circle_str += "Радиус: " + str(round(circle.radius, print_precision)) + '\n'
            else:
                circle_str = "Вторая окружность:\n"
                circle_str += "Координаты:\n" + "X: " + str(round(circle.x, print_precision)) + " Y: " + str(round(circle.y, print_precision)) + '\n'
                circle_str += "Радиус: " + str(round(circle.radius, print_precision)) + '\n'
            if index % 2 == 0:
                height_str = "\nКоордината Y касательной: " + str(round(heights[(index - 1) // 2], print_precision)) + "\n\n"

            str_answer += circle_str + height_str

            index += 1
        messagebox.showinfo("Решение", str_answer)

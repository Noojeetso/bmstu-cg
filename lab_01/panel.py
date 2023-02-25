from tkinter import *
from storage import Point


class PointFrame(Frame):
    """ Frame that store point coordinates """
    point: Point
    widgets: list[Widget]

    def __init__(self, master: Frame, point: Point):
        super().__init__(master)

        self.point = point
        self.widgets = list()

        self.pack(side=TOP, expand=True, fill=BOTH)

        content_frame = Frame(self)
        content_frame.pack(side=RIGHT, expand=True, fill=BOTH)
        self.widgets.append(content_frame)

        delete_button = Button(self, text='Delete', width=7)
        delete_button.pack(side=RIGHT, fill=BOTH)
        self.widgets.append(delete_button)

        self.create_x_y_input(content_frame)

        delete_button.config(command=self.remove_frame)

    def remove_frame(self):
        """ Remove point panel frame by button click """
        self.event_generate("<<OnRemove>>")
        # self.destroy()

    def destroy(self):
        """ Destroy point panel frame """
        for widget in self.widgets:
            widget.destroy()
        super().destroy()

    def update_coordinate(self, symbol, event):
        """ Update coordinates from input fields """
        str_value = event.widget.get()
        try:
            value = float(str_value)
        except ValueError:
            return
        if symbol == 'x':
            self.point.x = value
        elif symbol == 'y':
            self.point.y = value
        else:
            return
        self.event_generate("<<OnMove>>")

    def create_x_y_input(self, master: Frame):
        """ Create point panel frame """
        coordinates_frame = Frame(master)
        coordinates_frame.pack(side=TOP, expand=True, fill=BOTH)
        self.widgets.append(coordinates_frame)

        for i, symbol in enumerate("xy"):
            if symbol == 'x':
                input_field = Entry(coordinates_frame, width=5, textvariable=self.point.x_var)
            else:
                input_field = Entry(coordinates_frame, width=5, textvariable=self.point.y_var)

            input_field.pack(side=LEFT, expand=True, fill=BOTH)
            input_field.bind('<KeyRelease>',
                             lambda event, symbol_=symbol:
                             self.update_coordinate(symbol_, event))
            self.widgets.append(input_field)


class Panel(Frame):
    points: list[Point]
    point_frames: list[PointFrame]
    precision: int

    def __init__(self, side, precision):
        super().__init__()

        self.points = list()
        self.point_frames = list()
        self.precision = precision

        # CREATE interaction panel container
        self.pack(side=side, expand=False, fill=BOTH)

        # CREATE part of the panel for INTERACTION with POINTS
        points_panel = Frame(self)
        points_panel.pack(side=TOP, expand=True, fill=BOTH)

        coordinates_frame = Frame(points_panel, width=int(1440 * 0.2))
        coordinates_frame.pack(side=TOP, expand=False, fill=BOTH)

        x_var = DoubleVar()
        y_var = DoubleVar()

        add_point = Button(coordinates_frame, text="➕ New point",
                           command=lambda: self.create_point_frame(x_var.get(), y_var.get()))
        add_point.pack(side=LEFT, expand=False, fill=BOTH)

        for i, symbol in enumerate("xy"):
            if symbol == 'x':
                input_field = Entry(coordinates_frame, textvariable=x_var, width=3)
                label = Label(coordinates_frame, text="X:")
            else:
                input_field = Entry(coordinates_frame, textvariable=y_var, width=3)
                label = Label(coordinates_frame, text="Y:")

            label.pack(side=LEFT, expand=False, fill=BOTH)
            input_field.pack(side=LEFT, expand=True, fill=BOTH)

        # CREATE SCROLLBAR for POINTS coordinates
        self.points_coordinates_container = Frame(points_panel)

        points_coordinates_canvas = Canvas(self.points_coordinates_container, width=1440 * 0.2, height=700)
        scrollbar = Scrollbar(self.points_coordinates_container,
                              orient="vertical", command=points_coordinates_canvas.yview)

        self.points_coordinates_frame = Frame(points_coordinates_canvas)
        self.points_coordinates_frame.bind("<Configure>", lambda event: points_coordinates_canvas.configure(
            scrollregion=points_coordinates_canvas.bbox("all")))

        points_canvas_frame = points_coordinates_canvas.create_window((0, 0),
                                                                      window=self.points_coordinates_frame, anchor="nw")
        points_coordinates_canvas.bind('<Configure>',
                                       lambda event: points_coordinates_canvas.itemconfig(points_canvas_frame,
                                                                                          width=event.width))
        points_coordinates_canvas.configure(yscrollcommand=scrollbar.set)

        self.points_coordinates_container.pack(side=LEFT, expand=False, fill=BOTH)
        points_coordinates_canvas.pack(side=LEFT, expand=False, fill=BOTH)
        scrollbar.pack(side=RIGHT, fill="y")

    def create_point_frame(self, x: float, y: float):
        point = Point(x, y)

        self.points.append(point)
        point_frame = PointFrame(self.points_coordinates_frame, point)
        self.point_frames.append(point_frame)
        point_frame.bind("<<OnRemove>>", lambda event: self.remove_point_frame(point_frame))
        point_frame.bind("<<OnMove>>", lambda event: self.move_point(point_frame))
        self.event_generate("<<OnAppend>>")

    def remove_point_frame(self, point_frame: PointFrame):
        self.points.remove(point_frame.point)
        self.point_frames.remove(point_frame)
        point_frame.destroy()
        self.event_generate("<<OnRemove>>")

    def move_point(self, point_frame: PointFrame):
        index = self.point_frames.index(point_frame)
        point_frame.point.x = round(point_frame.point.x, self.precision)
        point_frame.point.y = round(point_frame.point.y, self.precision)
        point_frame.point.x_var.set(point_frame.point.x)
        point_frame.point.y_var.set(point_frame.point.y)
        self.event_generate("<<OnMove>>", state=index)

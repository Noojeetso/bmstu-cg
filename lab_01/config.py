import os.path


class Config:
    point_color: str
    fields: dict

    def set_parameters(self):
        self.fields = dict({"point_color": "#56b133", "point_radius": 5, "triangle_point_color": "#e59c94",
                            "triangle_point_radius": 5, "triangle_line_color": "#00b9b9", "triangle_line_width": 3,
                            "connection_line_color": "#c387ec", "connection_line_width": 3, "cursor_catch_radius": 20})

        if not os.path.isfile(".config"):
            self.create_config()
            print("config file was created")
        elif os.path.isfile(".config"):
            with open(".config", 'r') as config_file:
                for line in config_file:
                    item = line.split(" ")
                    if len(item) != 2:
                        continue
                    key, value = item
                    if key in self.fields.keys():
                        self.point_color = "#56b133"
                        # print("self." + key + ' = ' + value)
                        try:
                            value = int(value)
                            self.fields.update({key: value})
                        except ValueError:
                            self.fields.update({key: value})
                        # exec("self." + key + ' = ' + value)
            print("config file was read")

    def create_config(self):
        with open(".config", 'w') as config_file:
            for key, value in self.fields.items():
                if type(value) == str:
                    config_file.write(key + ' "' + str(value) + '"\n')
                else:
                    config_file.write(key + ' ' + str(value) + '\n')

import os.path


class Config:
    point_color: str
    fields: dict

    def __init__(self):
        self.fields = dict({"point_color": "#56b133", "point_radius": 5,
                            "bg_color": "#BDDEA9", "fg_color": "#E5BA73", "active_bg_color": "#C58940",
                            "graph_bg_color": "#EDECB6", "field_color": "white", "grid_line_color": "cyan",
                            "cursor_catch_radius": 20})

        if not os.path.isfile(".config"):
            self.create_config()
            print("config file was created")
        elif os.path.isfile(".config"):
            with open(".config", 'r') as config_file:
                for line in config_file:
                    line = line.rstrip()
                    item = line.split(" ")
                    if len(item) != 2:
                        continue
                    key, value = item
                    # print("item:", key, value)
                    if key in self.fields.keys():
                        self.point_color = "#56b133"
                        # print("self." + key + ' = ' + value)
                        try:
                            value = int(value)
                            self.fields.update({key: value})
                        except ValueError:
                            self.fields.update({key: value})
                        # exec("self." + key + ' = ' + value)
            print(self.fields.get("grid_line_color"))
            print("config file was read")

    def create_config(self):
        with open(".config", 'w') as config_file:
            for key, value in self.fields.items():
                if type(value) == str:
                    config_file.write(key + ' "' + str(value) + '"\n')
                else:
                    config_file.write(key + ' ' + str(value) + '\n')

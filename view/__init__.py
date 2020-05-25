import matplotlib.pyplot as plt
from os import system, name



class SingletonMeta(type):
    _instance = None

    def __call__(cls):
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class View(object):
    def __init__(self, subsystems_controller):
        self.__subsystems_controller = subsystems_controller

    def draw_menu(self, menu_headline: str, menu_list: list):
        self.preparation()
        print(menu_headline)
        number = 0
        for menu_item in menu_list:
            # additional = special_parameters.get(menu_item)
            # if additional is not None:
            #     add = additional(self.__subsystems_controller.data_backup_system_activity)
            # print(f" {number}: {menu_item}{additional if additional is not None else ''}")
            print(f" {number}: {menu_item}")
            number += 1

    def show_error(self, msg: str):
        print("Error: " + msg)

    def preparation(self):
        print("\033[H\033[J")

    def show_graph(self, title: str, data: dict, name: str):
        values = [int(x) for x in data.values()]
        keys = list(data.keys())

        # range_of_list_values = abs(max(values) - min(values))
        # radius = range_of_list_values / 10
        # length = len(values)
        # step = int(length / 5)
        # yticks = [values[0]]
        # for i in range(1, 6):
        #     val_i = values[i * step]
        #     if abs(yticks[-1] - val_i) >= radius:
        #         yticks.append(values[i * step])
        #     else:
        #         for j in range(1, step):
        #             val_j = values[i * step + j]
        #             if abs(yticks[-1] - val_j) >= radius:
        #                 yticks.append(values[i * step + j])
        #                 break

        row = 5
        range_of_list_values = abs(max(values) - min(values))
        radius = int(range_of_list_values / row)
        yticks = [min(values)]
        for i in range(1, row):
            yticks.append(i * radius)
        yticks.append(max(values))


        length = len(values)
        step = int(length / 5)
        xticks = [keys[x * int(step)] for x in range(0, 6)]

        plt.suptitle(title)
        plt.plot(keys, values)
        plt.ylabel(name)
        if range_of_list_values > 60:
            plt.yticks(yticks)
        plt.xlabel('Data')
        plt.xticks(xticks)
        plt.show()


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
            print(f" {number}: {menu_item}")
            number += 1

    def show_error(self, msg: str):
        print("Error: " + msg)

    def preparation(self):
        print("\033[H\033[J")

    def show_graph(self, title: str, data: dict, name: str, mode: str):
        values = [int(x) for x in data.values()]
        keys = list(data.keys())
        plt.figure(figsize=(12, 7))
        plt.suptitle(title)
        if mode == 'bar':
            plt.bar(keys, values)
        elif mode == 'plot':
            plt.plot(keys, values)
        else:
            Exception('Invalid graph mode')
        plt.xticks(keys[::5], rotation='vertical')
        plt.ylabel(name)
        plt.xlabel('Date')
        plt.show()

    def show_pie(self, title: str, data: dict):
        plt.title(title)
        new_data = {}
        for key, value in data.items():
            if int(value) != 0:
                new_data[key] = value
        if len(new_data) != 0:
            plt.pie(new_data.values(), labels=new_data.keys(), autopct=autopct_format(new_data.values()))
            plt.show()
        else:
            Exception('no data')


def autopct_format(values):
    def my_format(pct):
        total = sum([int(value) for value in values])
        val = int(round(pct * total / 100.0))
        return '{v:d}'.format(v=val)

    return my_format


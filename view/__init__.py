import matplotlib.pyplot as plt

from os import system, name


class View(object):
    def __init__(self):
        print("view")
        # plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        # plt.ylabel('some numbers')
        # plt.show()

    def draw_menu(self, menu_headline: str, menu_list: list):
        self.clear()
        print(menu_headline)
        number = 0
        for menu_item in menu_list:
            print(f" {number}: {menu_item}")
            number += 1

    def error(self, msg: str):
        print("Error: " + msg)

    def clear(self):
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

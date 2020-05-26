import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import heapq
from scipy import stats
from os import system, name


class SingletonMeta(type):
    _instance = None

    def __call__(cls):
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class View(object):
    def __init__(self, subsystems_controller):
        self._subsystems_controller = subsystems_controller

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
        print("Mean: ", np.mean(values))
        print("Median: ", np.median(values))
        print("Mode: ", stats.mode(values))
        print("Max: ", np.max(values, axis=0))
        plt.show()

    def additional_task(self, title: str, name: str, data: dict):
        values = list(data.values())
        nlarges = heapq.nlargest(6, values)
        keys = list(data.keys())
        new_keys = []
        for key, value in data.items():
            if value in nlarges:
                new_keys.append(key)

        plt.figure(figsize=(16, 9))
        plt.plot(keys, values)
        plt.suptitle(f"Показник параметру:{name} для кожної з країн")
        plt.xticks(new_keys, rotation='vertical')
        plt.ylabel(name)
        plt.xlabel('Countries')
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
            raise Exception('Nothing happened at that day')

    def regression(self, data: dict, key):
        values = list(data.values())
        x = np.array([value.get(f"Total{key}") for value in values]).astype(int)

        latitude = [float(value.get('Latitude')) for value in values]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, latitude)
        plt.figure(figsize=(12, 7))
        plt.title(f"Регресія залежності параметру: {key} відносно широти країн")
        plt.plot(x, latitude, 'ob')
        plt.plot(x, intercept + slope * x, 'r')
        plt.show()

        latitude = [float(value.get('Latitude')) for value in values]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, latitude)
        plt.figure(figsize=(12, 7))
        plt.title(f"Регресія залежності параметру: {key} відносно широти країн")
        plt.plot(x, latitude, 'ob')
        plt.plot(x, intercept + slope * x, 'ro')
        plt.xscale('log')
        plt.show()

        longitude = [float(value.get('Longitude')) for value in values]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, longitude)
        plt.figure(figsize=(12, 7))
        plt.title(f"Регресія залежності параметру: {key} відносно довготи країн")
        plt.plot(x, longitude, 'ob')
        plt.plot(x, intercept + slope * x, 'r')
        plt.show()

        longitude = [float(value.get('Longitude')) for value in values]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, longitude)
        plt.figure(figsize=(12, 7))
        plt.title(f"Регресія залежності параметру: {key} відносно довготи країн")
        plt.plot(x, longitude, 'ob')
        plt.xscale('log')
        plt.plot(x, intercept + slope * x, 'ro')
        plt.show()


def autopct_format(values):
    def my_format(pct):
        total = np.sum([int(value) for value in values])
        val = int(round(pct * total / 100.0))
        return '{v:d}'.format(v=val)

    return my_format



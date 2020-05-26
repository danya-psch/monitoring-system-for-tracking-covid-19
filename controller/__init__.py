import datetime
from datetime import date

import numpy as np

from redis_server import RedisServer
from subsystems import SubSystemsController
from view import View
import glob


class Controller(object):
    def __init__(self):
        self._menu_config = {
            '': ''
        }
        self._rserver = RedisServer()
        self._subsystems_controller = SubSystemsController(self._rserver)
        self._view = View(self._subsystems_controller)
        self._menu = 'Main menu'
        self._path = ['Main menu']
        self._loop = True
        self.start()

    def start(self):
        try:
            from menu_list import menu_list
            while self._loop:
                choice = self.make_choice(self._menu, menu_list[self._menu].keys())
                self.consider_choice(self, choice, list(menu_list[self._menu].values()))
        except Exception as e:
            self._view.show_error(str(e))

    def make_choice(self, menu_headline: str, menu_list: list):
        self._view.draw_menu(menu_headline, menu_list)
        return Controller._get_uint_value("Make your choice: ", len(menu_list))

    def consider_choice(self, controller, choice: int, list_of_func: list):
        if choice > len(list_of_func) - 1:
            raise Exception("func is not exist")

        desired_func = list_of_func[choice]
        desired_func(controller)

    def statistics_total(self):
        try:
            country = self._get_str_from_list_value("Enter country", self._subsystems_controller.get_countries_list())
            key = self._get_str_from_list_value("Enter mode", ['Confirmed', 'Deaths', 'Recovered'])
            data = self._rserver.get_total_by_name(key, country)
            if len(data) == 0:
                raise Exception('no data')
            self._view.show_graph(country, data, key, 'plot')
        except Exception as e:
            self._view.show_error(str(e))

    def statistics(self):
        try:
            country = self._get_str_from_list_value("Enter country",
                                                     self._subsystems_controller.get_countries_list())
            key = self._get_str_from_list_value("Enter mode", ['Confirmed', 'Deaths', 'Recovered'])
            data = self._rserver.get_daily_by_name(key, country)
            if len(data) == 0:
                raise Exception('no data')
            self._view.show_graph(country, data, key, 'bar')
        except Exception as e:
            self._view.show_error(str(e))

    def day_statistics(self):
        country = self._get_str_from_list_value("Enter country",
                                                 self._subsystems_controller.get_countries_list())
        date_range = self._rserver.get_range_of_date_for_country(country)
        given_date = self._get_date_value("Enter date", date_range)
        data = self._rserver.get_all_day_by_country(country, str(given_date))
        self._view.show_pie("Statistics for the day", data)

    def regression(self):
        countries = self._rserver.get_countries_with_data()
        given_key = self._get_str_from_list_value("Enter mode", ['Confirmed', 'Deaths', 'Recovered'])
        keys_for_delete = []
        for key, statistics_data in countries.items():
            if 'Latitude' not in statistics_data or 'Longitude' not in statistics_data:
                keys_for_delete.append(key)

        for key in keys_for_delete:
            del countries[key]
        self._view.regression(countries, given_key)

    def countries_statistics(self):
        countries = self._rserver.get_countries_with_data()
        given_key = self._get_str_from_list_value("Enter mode", ['Confirmed', 'Deaths', 'Recovered'])
        mode = self._get_str_from_list_value("Enter mode", ['Mean', 'Median', 'Max'])
        data = {}
        for country in countries:
            values = [int(x) for x in self._rserver.get_daily_by_name(given_key, country).values()]
            if len(values) != 0:
                if mode == 'Mean':
                    data[country] = np.mean(values)
                elif mode == 'Median':
                    data[country] = np.median(values)
                elif mode == 'Max':
                    data[country] = np.max(values)
                else:
                    raise Exception('Invalid mode in countries statistics func')
        self._view.additional_task("", mode, data)

    def back(self):
        self._path.pop()
        self._menu = self._path[-1]

    def generate_data(self):
        self._subsystems_controller.generate_data()

    def backup_data(self):
        self._subsystems_controller.backup_data()

    def recovery_data(self):
        file = self._get_str_from_list_value('Enter file', [file[8:] for file in glob.glob("./dumps/*.json")])
        self._subsystems_controller.recovery_data(file)

    @staticmethod
    def _get_uint_value(msg: str, top_line: int = None):
        while True:
            number = input(msg)
            if number.isdigit():
                number = int(number)
                if top_line is None or 0 <= number < top_line:
                    return number

    def _get_str_from_list_value(self, msg: str, ls: list):
        while True:
            country = input(f"{msg}{'(' + ', '.join(x for x in ls) + ')' if len(ls) <= 5 else ''}: ")
            if country in ls:
                return country
            self._view.show_error('There is not item like that, try again!')

    def _get_date_value(self, msg: str, date_range=None):
        while True:
            try:
                usr_input = input(f"{msg}, date should be in range {date_range.get('start')} - {date_range.get('end')} "
                                  f"(format of date: YYYY-MM-DD): ") \
                    if date_range is not None else input(f"{msg} (format of date: YYYY-MM-DD): ")
                usr_date = date(*map(int, usr_input.split('-')))
                if date_range is not None:
                    if date(*map(int, date_range.get('start').split('-'))) <= usr_date <= date(*map(int, date_range.get('end').split('-'))):
                        return usr_date
                else:
                    return usr_date
                self._view.show_error('Date out of range, try again!')
            except Exception as e:
                self._view.show_error(str(e))

    def change_data_backup_status(self):
        self._subsystems_controller.data_backup_system_activity =\
            not self._subsystems_controller.data_backup_system_activity

    def stop_loop(self):
        self._loop = False


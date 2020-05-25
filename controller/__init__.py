from datetime import date

from redis_server import RedisServer
from subsystems import SubSystemsController
from view import View
import glob


class Controller(object):
    def __init__(self):
        self.__menu_config = {
            '': ''
        }
        self.__rserver = RedisServer()
        self.__subsystems_controller = SubSystemsController(self.__rserver)
        self.__view = View(self.__subsystems_controller)
        self.__menu = 'Main menu'
        self.__path = ['Main menu']
        self.__loop = True
        self.start()

    def start(self):
        try:
            from menu_list import menu_list
            while self.__loop:
                choice = self.make_choice(self.__menu, menu_list[self.__menu].keys())
                self.consider_choice(self, choice, list(menu_list[self.__menu].values()))
        except Exception as e:
            self.__view.show_error(str(e))

    def make_choice(self, menu_headline: str, menu_list: list):
        self.__view.draw_menu(menu_headline, menu_list)
        return Controller.__get_uint_value("Make your choice: ", len(menu_list))

    def consider_choice(self, controller, choice: int, list_of_func: list):
        if choice > len(list_of_func) - 1:
            raise Exception("func is not exist")

        desired_func = list_of_func[choice]
        desired_func(controller)

    def statistics_total(self):
        try:
            country = self.__get_str_from_list_value("Enter country", self.__subsystems_controller.get_countries_list())
            key = self.__get_str_from_list_value("Enter mode", ['Confirmed', 'Deaths', 'Recovered'])
            data = self.__rserver.get_total_by_name(key, country)
            if len(data) == 0:
                raise Exception('no data')
            self.__view.show_graph(country, data, key, 'plot')
        except Exception as e:
            self.__view.show_error(str(e))

    def statistics(self):
        try:
            country = self.__get_str_from_list_value("Enter country",
                                                     self.__subsystems_controller.get_countries_list())
            key = self.__get_str_from_list_value("Enter mode", ['Confirmed', 'Deaths', 'Recovered'])
            data = self.__rserver.get_daily_by_name(key, country)
            if len(data) == 0:
                raise Exception('no data')
            self.__view.show_graph(country, data, key, 'bar')
        except Exception as e:
            self.__view.show_error(str(e))

    def day_statistics(self):
        country = self.__get_str_from_list_value("Enter country",
                                                 self.__subsystems_controller.get_countries_list())
        date_range = self.__rserver.get_range_of_date_for_country(country)
        given_date = self.__get_date_value("Enter date", date_range)
        data = self.__rserver.get_all_day_by_country(country, str(given_date))
        self.__view.show_pie("Statistics for the day", data)

    def back(self):
        self.__path.pop()
        self.__menu = self.__path[-1]

    def generate_data(self):
        self.__subsystems_controller.generate_data()

    def backup_data(self):
        self.__subsystems_controller.backup_data()

    def recovery_data(self):
        file = self.__get_str_from_list_value('Enter file', [file[8:] for file in glob.glob("./dumps/*.json")])
        self.__subsystems_controller.recovery_data(file)

    @staticmethod
    def __get_uint_value(msg: str, top_line: int = None):
        while True:
            number = input(msg)
            if number.isdigit():
                number = int(number)
                if top_line is None or 0 <= number < top_line:
                    return number

    def __get_str_from_list_value(self, msg: str, ls: list):
        while True:
            country = input(f"{msg}{'(' + ', '.join(x for x in ls) + ')' if len(ls) <= 5 else ''}: ")
            if country in ls:
                return country
            self.__view.show_error('There is not country like that, try again!')

    def __get_date_value(self, msg: str, date_range):
        while True:
            try:
                usr_input = input(f"{msg}, date should be in range {date_range.get('start')} - {date_range.get('end')} "
                                  f"(format of date: YYYY-MM-DD): ")
                usr_date = date(*map(int, usr_input.split('-')))
                if date(*map(int, date_range.get('start').split('-'))) <= usr_date <= date(*map(int, date_range.get('end').split('-'))):
                    return usr_date
                self.__view.show_error('Date out of range, try again!')
            except Exception as e:
                self.__view.show_error(str(e))

    def change_data_backup_status(self):
        self.__subsystems_controller.data_backup_system_activity =\
            not self.__subsystems_controller.data_backup_system_activity

    def stop_loop(self):
        self.__loop = False
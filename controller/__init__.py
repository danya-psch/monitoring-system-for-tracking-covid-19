from redis_server import RedisServer
from subsystems import SubSystemsController
from view import View


class Controller(object):
    def __init__(self):
        self.__view = View() # redo
        self.__rserver = RedisServer()
        self.__subsystems_controller = SubSystemsController(self.__rserver)
        self.__menu = 'Main menu'
        self.__loop = True
        # self.start()

    def start(self):
        try:
            from menu_list import menu_list
            while self.__loop:
                choice = self.make_choice(self.__menu, menu_list[self.__menu].keys())
                self.consider_choice(self, choice, list(menu_list[self.__menu].values()))
        except Exception as e:
            self.__view.error(str(e))

    def make_choice(self, menu_headline: str, menu_list: list):
        self.__view.draw_menu(menu_headline, menu_list)
        return Controller.get_uint_value("Make your choice: ", len(menu_list))

    def consider_choice(self, controller, choice: int, list_of_func: list):
        if choice > len(list_of_func) - 1:
            raise Exception("func is not exist")

        desired_func = list_of_func[choice]
        desired_func(controller)

    def subsystems_settings(self):
        print('subsystems_settings')

    @staticmethod
    def get_uint_value(msg: str, top_line: int = None):
        while True:
            number = input(msg)
            if number.isdigit():
                number = int(number)
                if top_line is None or 0 <= number < top_line:
                    return number

    def stop_loop(self):
        self.__loop = False
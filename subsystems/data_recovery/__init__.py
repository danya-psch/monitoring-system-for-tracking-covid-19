import json


class DataRecoverySystem(object):
    def __init__(self, rserver):
        self.__rserver = rserver

    def start(self):
        with open('data_recovery_file.dat', 'r') as file:
            res = json.load(file)
            if isinstance(res, dict) and 'type' in res and 'data' in res:
                switcher = {
                    'hmset': self.__write_down
                }
                switcher.get(res.get(type))(res.get('data'))

    def __write_down(self, data: list):
        self.__rserver.write_down(data, False)



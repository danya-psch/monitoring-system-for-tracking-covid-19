import json


class DataBackupSystem(object):
    def __init__(self, rserver, active, truncate: bool):
        self.__rserver = rserver
        mode = 'w' if truncate else 'a'
        self.__file = open('data_recovery_file.dat', mode)
        self.__active = active

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool):
        self.__active = value

    def write_down(self, type, data):
        if self.__active:
            json.dump({'type': type, 'data': data}, self.__file)
            self.__file.write("\n")






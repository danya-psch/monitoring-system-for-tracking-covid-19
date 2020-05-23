class DataBackupSystem(object):
    def __init__(self):
        self.__active = True

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool):
        self.__active = value

    def write_down(self, data):
        print("write_down")



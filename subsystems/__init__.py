from redis_server import RedisServer
from subsystems.data_backup import DataBackupSystem
from subsystems.data_generation import DataGenerationSystem
from subsystems.data_validation import DataValidationSystem


class SubSystemsController(object):
    def __init__(self, redis_server: RedisServer):
        self.__rserver = redis_server

        self.__data_backup_system = DataBackupSystem(self.__rserver)
        self.__rserver.set_data_backup_system(self.__data_backup_system)

        self.__data_validation_system = DataValidationSystem()
        self.__data_generation_system = DataGenerationSystem(self.__rserver, self.__data_validation_system)

    @property
    def dbs(self) -> DataBackupSystem:
        return self.__data_backup_system

    @property
    def dgs(self) -> DataGenerationSystem:
        return self.__data_generation_system

    @property
    def dvs(self) -> DataValidationSystem:
        return self.__data_validation_system

    def backup_data(self):
        self.__data_backup_system.backup()

    def recovery_data(self, file: str):
        self.__data_backup_system.recovery(file)

    def generate_data(self):
        self.__data_generation_system.start()

    def get_countries_list(self):
        return self.__data_generation_system.get_countries()

    def save(self):
        self.__rserver.save()

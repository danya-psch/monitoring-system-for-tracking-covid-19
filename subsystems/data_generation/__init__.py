from redis_server import RedisServer
# from subsystems import DataValidationSystem
from subsystems.data_generation.requests_to_api import *


class DataGenerationSystem(object):
    def __init__(self, redis_server: RedisServer, data_validation_system):
        self.__rserver = redis_server
        self.__data_validation_system = data_validation_system

        self.__mode = lambda func, params=[]: {
            'type': func.__name__,
            'data': func(*params)
        }

    def start(self):
        self._generate_countries()
        self._generate_daily_statistics_for_countries()
        self._generate_total_daily_statistics_for_countries()

    def get_countries(self) -> list:
        generated_data = self.__mode(get_countries)
        return self.__data_validation_system.validate_data(**generated_data)

    def _generate_countries(self):
        generated_data = self.__mode(get_summary)
        validated_data = self.__data_validation_system.validate_data(**generated_data)
        for country in validated_data:
            self.__rserver.write_down(country)

    def _generate_daily_statistics_for_countries(self):
        countries = self.get_countries()
        for country in countries:
            self._generate_daily_statistics_for_country(country)

    def _generate_daily_statistics_for_country(self, country):
        generated_data = self.__mode(get_total_day_one, [country])
        generated_data['type'] = 'daily'
        validated_data = self.__data_validation_system.validate_data(**generated_data)
        for day in validated_data:
            self.__rserver.write_down(day)

    def _generate_total_daily_statistics_for_countries(self):
        countries = self.get_countries()
        for country in countries:
            self._generate_total_daily_statistics_for_country(country)

    def _generate_total_daily_statistics_for_country(self, country):
        generated_data = self.__mode(get_total_day_one, [country])
        validated_data = self.__data_validation_system.validate_data(**generated_data)
        for day in validated_data:
            self.__rserver.write_down(day)

    def __generate_summary(self):
        return self.__mode(get_summary)





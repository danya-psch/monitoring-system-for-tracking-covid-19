from redis_server import RedisServer
from subsystems.data_validation import DataValidationSystem
from subsystems.data_generation.requests_to_api import *
from lat_lng_data import lat_lng


class DataGenerationSystem(object):
    def __init__(self, redis_server: RedisServer, data_validation_system: DataValidationSystem):
        self._rserver = redis_server
        self._data_validation_system = data_validation_system

        self._mode = lambda func, params=[]: {
            'type': func.__name__,
            'data': func(*params)
        }

    def start(self):
        self._generate_countries()
        # self._generate_daily_statistics_for_countries()
        # self._generate_total_daily_statistics_for_countries()

    def get_countries(self) -> list:
        generated_data = self._mode(get_countries)
        return self._data_validation_system.validate_data(**generated_data)

    def _generate_countries(self):
        generated_data = self._mode(get_summary)
        validated_data = self._data_validation_system.validate_data(**generated_data)
        for country in validated_data:
            code = country[1].get('CountryCode')
            if lat_lng.get(code) is not None:
                country[1]['Latitude'] = lat_lng.get(code)['latitude']
                country[1]['Longitude'] = lat_lng.get(code)['longitude']
            self._rserver.write_down(country)

    def _generate_daily_statistics_for_countries(self):
        countries = self.get_countries()
        for country in countries:
            self._generate_daily_statistics_for_country(country)

    def _generate_daily_statistics_for_country(self, country):
        generated_data = self._mode(get_daily_for_country, [country])
        validated_data = self._data_validation_system.validate_data(**generated_data)
        for day in validated_data:
            self._rserver.write_down(day)

    def _generate_total_daily_statistics_for_countries(self):
        countries = self.get_countries()
        for country in countries:
            self._generate_total_daily_statistics_for_country(country)

    def _generate_total_daily_statistics_for_country(self, country):
        generated_data = self._mode(get_total_for_country, [country])
        validated_data = self._data_validation_system.validate_data(**generated_data)
        for day in validated_data:
            self._rserver.write_down(day)

    def _generate_summary(self):
        return self._mode(get_summary)





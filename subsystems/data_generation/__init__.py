from redis_server import RedisServer
from subsystems.data_generation.requests_to_api import *


class DataGenerationSystem(object):
    def __init__(self, redis_server: RedisServer):
        self.__rserver = redis_server

    def generate_countries(self):
        return {
            'type': 'generate_countries',
            'data': get_countries()
        }

    def generate_summary(self):
        return {
            'type': 'generate_summary',
            'data': get_summary()
        }

    def get_total_day_one(self, country):
        return {
            'type': 'get_total_day_one',
            'data': get_total_day_one(country)
        }




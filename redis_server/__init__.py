import redis
from rediscluster import RedisCluster
from datetime import datetime


class RedisServer(object):
    def __init__(self):
        startup_nodes = [
            {"host": "127.0.0.1", "port": "7000"},
            {"host": "127.0.0.1", "port": "7001"},
            {"host": "127.0.0.1", "port": "7002"}
        ]
        self.__rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        # self.__rc = redis.Redis(charset="utf-8", decode_responses=True)
        self.__data_backup_system = None

    @property
    def rc(self):
        return self.__rc

    # from subsystems.data_backup import DataBackupSystem
    def set_data_backup_system(self, data_backup_system):
        self.__data_backup_system = data_backup_system

    def write_down(self, data: list):
        self.__rc.hmset(*data)

    def get_daily_by_name(self, key_str: str, name, date='*'):
        keys = self.__rc.keys(f"{name}:{date}")
        keys.sort()
        days = {}
        for key in keys:
            item = self.__rc.hgetall(key)
            country, date = map(str, key.split(':'))
            days[date[5:]] = item.get(key_str)
        return days

    def get_range_of_date_for_country(self, name, date='*'):
        keys = self.__rc.keys(f"{name}:{date}")
        keys.sort()
        return {
            'start': keys[0][len(name) + 1:],
            'end': keys[-1][len(name) + 1:]
        }

    def get_all_day_by_country(self, name, date='*'):
        key = self.__rc.keys(f"{name}:{date}")[0]
        return self.__rc.hgetall(key)

    def get_total_by_name(self, key_str: str, name, date='*'):
        keys = self.__rc.keys(f"total:{name}:{date}")
        keys.sort()
        days = {}
        for key in keys:
            item = self.__rc.hgetall(key)
            total_str, country, date = map(str, key.split(':'))
            days[date[5:]] = item.get(key_str)
        return days

    def save(self):
        self.__rc.save()

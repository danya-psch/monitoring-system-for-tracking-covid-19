import redis
from rediscluster import RedisCluster
from datetime import datetime


class RedisServer(object):
    def __init__(self):
        startup_nodes = [
            {"host": "172.24.0.2", "port": "7000"},
            {"host": "172.24.0.2", "port": "7001"},
            {"host": "172.24.0.2", "port": "7002"}
        ]
        # self.__rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        self.__rc = redis.Redis(charset="utf-8", decode_responses=True)
        self.__data_backup_system = None

    # from subsystems.data_backup import DataBackupSystem
    def set_data_backup_system(self, data_backup_system):
        self.__data_backup_system = data_backup_system

    def write_down(self, data: list, backup=True):
        self.__rc.hmset(*data)
        if self.__data_backup_system is not None and backup:
            self.__data_backup_system.write_down('hmset', data)

    def get_daily_by_name(self, name, key_str: str):
        data = self.__rc.keys(f"{name}:*")
        data.sort()
        # days = {
        #     'date': [],
        #     'value': []
        # }
        days = {}
        for key in data:
            item = self.__rc.hgetall(key)
            country, date = map(str, key.split(':'))
            days[date[5:]] = item.get(key_str)
            # days.get('date').append(date[5:])
            # days.get('value').append(item.get(key_str))
        return days

    def get_total_by_name(self, name, key_str):
        data = self.__rc.keys(f"total:{name}:*")
        data.sort()
        # days = {
        #     'date': [],
        #     'value': []
        # }
        days = {}
        for key in data:
            item = self.__rc.hgetall(key)
            total_str, country, date = map(str, key.split(':'))
            days[date[5:]] = item.get(key_str)

            # item = self.__rc.hgetall(key)
            # total_str, country, date = map(str, key.split(':'))
            # days.get('date').append(date[5:])
            # days.get('value').append(item.get(key_str))
        return days

    def save(self):
        self.__rc.save()

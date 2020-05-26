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
        self._rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        self._rs = redis.Redis(host='localhost', port=6379, db=0)
        # self._rc = redis.Redis(charset="utf-8", decode_responses=True)
        self._data_backup_system = None

    @property
    def rc(self):
        return self._rc

    def _check_for_sharding(self, country_name: str):
        if country_name is not None and len(country_name) > 0:
            if ord(country_name[0]) < 110:
                return self._rc
            else:
                return self._rs


    # from subsystems.data_backup import DataBackupSystem
    def set_data_backup_system(self, data_backup_system):
        self._data_backup_system = data_backup_system

    def get_country_data(self, country_name):
        r = self._check_for_sharding(country_name)
        key = r.keys(f"country:{country_name}")[0]
        return r.hgetall(key)

    def write_down(self, data: list):
        ls = data[0].lower().split(':')
        if len(ls) == 2 and ls[0] == 'country':
            r = self._check_for_sharding(ls[1])
            r.hmset(*data)
        else:
            self._rc.hmset(*data)


    def get_daily_by_name(self, key_str: str, name, date='*'):
        keys = self._rc.keys(f"{name}:{date}")
        keys.sort()
        days = {}
        for key in keys:
            item = self._rc.hgetall(key)
            country, date = map(str, key.split(':'))
            days[date[5:]] = item.get(key_str)
        return days

    def get_range_of_date_for_country(self, name, date='*'):
        keys = self._rc.keys(f"{name}:{date}")
        keys.sort()
        return {
            'start': keys[0][len(name) + 1:],
            'end': keys[-1][len(name) + 1:]
        }

    def get_countries_with_data(self):
        keys = self._rc.keys(f"country:*")
        contries = {}
        for key in keys:
            item = self._rc.hgetall(key)
            litter, country = map(str, key.split(':'))
            contries[country] = item
        return contries


    def get_all_day_by_country(self, name, date='*'):
        key = self._rc.keys(f"{name}:{date}")[0]
        return self._rc.hgetall(key)

    def get_total_by_name(self, key_str: str, name, date='*'):
        keys = self._rc.keys(f"total:{name}:{date}")
        keys.sort()
        days = {}
        for key in keys:
            item = self._rc.hgetall(key)
            total_str, country, date = map(str, key.split(':'))
            days[date[5:]] = item.get(key_str)
        return days

    def save(self):
        self._rc.save()

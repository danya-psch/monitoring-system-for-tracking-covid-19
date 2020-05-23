import redis
from rediscluster import RedisCluster
# from subsystems import DataBackupSystem


class RedisServer(object):
    def __init__(self):
        self.__rc = None
        self.__rs = redis.Redis(charset="utf-8", decode_responses=True)
        self.__data_backup_system = None
        # self.setup_server()

    def set_data_backup_system(self, data_backup_system):
        self.__data_backup_system = data_backup_system

    def set(self, name: str, value: str):
        self.__rc.set(name, value)

    def setup_server(self):
        self.__rs = redis.Redis(charset="utf-8", decode_responses=True)

    def setup_cluster(self):
        startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]
        self.__rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    def write_down(self, data: list):
        self.__rs.hmset(*data)
        if self.__data_backup_system is not None and self.__data_backup_system.active:
            self.__data_backup_system.write_down(data)


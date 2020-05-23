
import redis
from rediscluster import RedisCluster
from subsystems.data_backup import DataBackupSystem


class RedisServer(object):
    def __init__(self, data_backup_system: DataBackupSystem):
        startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]
        self.__rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        self.__data_backup_system = data_backup_system

    def set(self, name: str, value: str):
        self._rc.set(name, value)



import redis
from rediscluster import RedisCluster


class RedisServer(object):
    def __init__(self):
        startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]
        self._rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    def set(self, name: str, value: str):
        self._rc.set(name, value)

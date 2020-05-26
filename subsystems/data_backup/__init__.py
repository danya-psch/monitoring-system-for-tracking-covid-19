import json
from redis_server import RedisServer
import redisdl


class DataBackupSystem(object):
    def __init__(self, rserver: RedisServer):
        self._rserver = rserver
        with open(f"./dumps/num.txt", 'r') as fnum:
            self._num = int(fnum.readline())

    def backup(self):
        with open(f"./dumps/dump{self._num}.json", 'w') as f:
            self._write(f)
            self._num += 1
            with open(f"./dumps/num.txt", 'w') as fnum:
                fnum.write(str(self._num))

    def recovery(self, file: str):
        with open(f"./dumps/{file}") as f:
            self._load(f)

    def _load(self, fd):
        for line in fd.readlines():
            item = json.loads(line[:-2])
            if item.get('type') == 'hash':
                self._rserver.write_down(item.get('data'))

    def _write(self, fd):
        for item in self._reader():
            fd.write(item)
            fd.write('\n')

    def _reader(self, keys='*'):
        items = []
        for key in self._rserver.rc.keys(keys):
            type = self._rserver.rc.type(key)
            item = self._rserver.rc.hgetall(key)
            items.append(json.dumps({
                'type': type,
                'data': [key, item]
            }))
        return items

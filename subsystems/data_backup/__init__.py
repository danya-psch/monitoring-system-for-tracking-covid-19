import json
import redisdl


class DataBackupSystem(object):
    def __init__(self, rserver):
        self.__rserver = rserver
        with open(f"./dumps/num.txt", 'r') as fnum:
            self.__num = int(fnum.readline())

    def backup(self):
        with open(f"./dumps/dump{self.__num}.json", 'w') as f:
            self._write(f)
            self.__num += 1
            with open(f"./dumps/num.txt", 'w') as fnum:
                fnum.write(str(self.__num))

    def recovery(self, file: str):
        with open(f"./dumps/{file}") as f:
            self._load(f)

    def _load(self, fd):
        for line in fd.readlines():
            item = json.loads(line[:-2])
            if item.get('type') == 'hash':
                self.__rserver.write_down(item.get('data'))

    def _write(self, fd):
        for item in self._reader():
            fd.write(item)
            fd.write('\n')

    def _reader(self, keys='*'):
        items = []
        for key in self.__rserver.rc.keys(keys):
            type = self.__rserver.rc.type(key)
            item = self.__rserver.rc.hgetall(key)
            items.append(json.dumps({
                'type': type,
                'data': [key, item]
            }))
        return items

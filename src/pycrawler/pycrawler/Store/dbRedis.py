from dbInterface import dbInterface
import redis


class dbRedis(dbInterface):

    def __init__(self, param):
        if "host" not in param:
            param["host"] = "localhost"
        if "port" not in param:
            param["port"] = 6379
        if "db" not in param:
            param["db"] = 0
        self._rds = redis.Redis(host=param["host"], port=param["port"],
                                db=param["db"])

    def add(self, key, value):
        return self._rds.set(key, value)

    def adddict(self, key, mapping):
        return self._rds.hmset(key, mapping)

    def get(self, key):
        return self._rds.get(key)

    def getdict(self, key, secondkey):
        return self._rds.hget(key, secondkey)

    def has(self, key):
        return True if self._rds.get(key) else False

    def delete(self, key):
        return True if self._rds.delete(key) else False

    # TODO: figure out what to put here
    def close(self):
        pass

from dbInterface import dbInterface
import redis


class dbRedis(dbInterface):

    def __init__(self, param):
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

    # TODO: figure out what to put here
    def close(self):
        pass

from dbBDB import dbBDB
from dbRedis import dbRedis


class NoSQL:

    '''May need to synchronized on _db_instance for concurrent writing '''

    def __init__(self, dbtype="bdb", param={}):
        self._db_instance = None
        if dbtype == "bdb":
            if "path" in param:
                self._db_instance = dbBDB(param)
            else:
                param["path"] = "localhost"
                self._db_instance = dbBDB(param)
        elif dbtype == "redis":
            self._db_instance = dbRedis(param)
        else:
            raise ValueError("Unrecognized database type")

    def set(self, key, value):
        self._db_instance.add(key, value)

    def dictset(self, key, mapping):
        self._db_instance.adddict(key, mapping)

    def get(self, key):
        return self._db_instance.get(key)

    def dictget(self, key, secondkey):
        return self._db_instance.getdict(key, secondkey)

    def has(self, key):
        return self._db_instance.has(key)

    def close(self):
        if self._db_instance:
            self._db_instance.close()

    def __del__(self):
        self.close()

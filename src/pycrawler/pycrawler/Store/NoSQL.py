from dbBDB import dbBDB
from dbRedis import dbRedis
import cPickle as pk


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

    def delete(self, key):
        return self._db_instance.delete(key)

    def close(self):
        if self._db_instance:
            self._db_instance.close()

    def __del__(self):
        self.close()


class NoSQLDict(object):
    """ Implemented a dictionary-like object using NoSQL object
        This implementation is used in the situation where the dictionary needs
        to be write to disc regularly to prevent the failure of the node. But
        this funcionality is actually depends on the nosql database chosed. This
        class should also handle serialization and deserialization.
    """

    def __init__(self, dbtype="bdb", param={}):
        self._db_dict = NoSQL(dbtype, param)

    def get(self, key):
        if self._db_dict.has(key):
            return pk.loads(self._db_dict.get(key))
        return None

    def __getitem__(self, key):
        result = self._db_dict.get(key)
        if result:
            return pk.loads(result)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        string_value = pk.dumps(value)
        self._db_dict.set(key, string_value)

    def __delitem__(self, key):
        self._db_dict.delete(key)

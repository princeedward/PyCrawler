from dbInterface import dbInterface
import os.path
import cPickle as pickle
import bsddb


# TODO: Update the implementation
class dbBDB(dbInterface):

    def __init__(self, param):
        if "path" not in param or param["path"] == "localhost":
            self.db_path_ = "./local_db.db"
        else:
            if os.path.isfile(param["path"]):
                self.db_path_ = param["path"]
            else:
                raise ValueError("Database does not exist")
        self.db_ = bsddb.btopen(self.db_path_, 'c')

    def add(self, key, value):
        if not isinstance(key, str):
            key = pickle.dumps(key)
        if isinstance(value, str):
            data = "".join(["n", value])
        else:
            data = "".join(["p", pickle.dumps(value)])
        self.db_[key] = data
        self.db_.sync()

    def get(self, key):
        if not type(key) in str:
            key = pickle.dumps(key)
        if key in self.db_:
            data = self.db_[key]
            if data[0] == "n":
                return data[1:]
            else:
                data_obj = pickle.loads(data[1:])
                return data_obj
        else:
            return None

    def close(self):
        self.db_.close()

    def has(self, key):
        if not type(key) in str:
            key = pickle.dumps(key)
        if key in self.db_:
            return True
        else:
            return False

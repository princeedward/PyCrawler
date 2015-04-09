import dbInterface
import os.path
import cPickle as pickle
import bsddb

class dbBDB(dbInterface):
    def __init__(self, location):
        if location == "localhost":
            self.db_path_ = "./local_db.db"
        else:
            if os.path.isfile(location):
                self.db_path_ = location
            else:
                raise ValueError("Database does not exist")
        self.db_ = bsddb.btopen(self.db_path_, 'c')

    def add(self, key, value):
        if not type(key) is str:
            key = pickle.dumps(key)
        if type(value) is str:
            data = "".join(["n",value])
        else:
            data = "".join(["p",pickle.dumps(value)])
        self.db_[key] = data
        self.db_.sync()

    def get(self, key):
        if not type(key) in str:
            key = pickle.dumps(key)
        if self.db_.has_key(key):
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
        if self.db_.has_key(key):
            return True
        else:
            return False


import dbBDB

class NoSQL:
    '''May need to synchronized on db_instance_ for concurrent writing '''
    def __init__(self, dbtype = "bdb", dblocal = "localhost", dbport = 3306):
        if dbtype == "bdb":
            self.db_instance_ = BDB(dblocal)
        else:
            raise ValueError("Unrecognized database type")

    def set(self, key, value):
        self.db_instance_.add(key, value)

    def get(self, key):
        return self.db_instance_.get(key)

    def has(self, key):
        return self.db_instance_.has(key)

    def close(self):
        self.db_instance_.close()


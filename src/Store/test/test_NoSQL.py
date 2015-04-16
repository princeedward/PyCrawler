import unittest
from NoSQL import NoSQL

class test_nosql(unittest.TestCase):

    def test_database_type(self):
        param = {}
        # test wrong database type
        self.assertRaises(ValueError):
            db = NoSQL("rdeis", param)

        # test right database type

    def test_redis_init(self):
        # test bad init parameters
        param = {"host": "localhost", "port":6379, "db":0}
        try:
            db = NoSQL("redis", param)
        except Exception: #TODO: Change this to dictionary no key exception
            self.fail("Unexpected redis NoSQL instance init exception")
        # test no connection raise(if it actually raise)

    def test_redis_set_value(self):
        # ---- test set key value pairs -------
        # test no string type key and values
        # test concurrent set and get(different keys and same key)
        # test fast serialized set and get
        # test different database concurrent write

    def test_redis_set_dict(self):
        # ---- test set key dict pairs
        # test bad input data types
        # test concurrent set and get
        # test fast serialized set and get
        # test different database concurrent write

    def test_redis_destruct(self):
        # destruct should not raise error
